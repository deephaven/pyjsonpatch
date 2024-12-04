from copy import deepcopy
from typing import Any

from .types import ApplyResult, Operation
from .utils import unescape_json_ptr


def get_by_ptr(obj: Any, ptr: str) -> ApplyResult:
    """
    Retrieves a value from an object  based on RFC 9601 (https://datatracker.ietf.org/doc/html/rfc6901).

    :param obj: The Python object, representing a JSON
    :param ptr: The pointer, based on RFC 9601
    :return: An `ApplyResult` with the value at the pointer
    """

    if ptr == "":
        return ApplyResult(obj=obj)
    return apply_operation(obj, {"op": "_get", "path": ptr})


def apply_operation(obj: Any, op: Operation, *, mutate: bool = True) -> ApplyResult:
    """
    Applies a JSON patch operation on an object, based on RFC 6902 (https://datatracker.ietf.org/doc/html/rfc6902).

    :param obj: The Python object, representing a JSON
    :param op: The operation to apply
    :param mutate: If `True`, the object will be mutated if possible. If `False`, the object never be mutated.
    :return: An `ApplyResult` with the root of the result and the removed object (if any)
    """

    if op["path"] == "":
        if op["op"] == "add":
            return ApplyResult(obj=op["value"])
        if op["op"] == "remove":
            return ApplyResult(obj=None, removed=obj)
        if op["op"] == "replace":
            return ApplyResult(obj=op["value"], removed=obj)
        if op["op"] == "move" or op["op"] == "copy":
            return ApplyResult(obj=get_by_ptr(obj, op["from"]).obj)
        if op["op"] == "test":
            if obj != op["value"]:
                raise AssertionError("Test operation failed")
            return ApplyResult(obj=obj)
        if op["op"] == "_get":
            return ApplyResult(obj=obj)
        raise ValueError(f"'{op['op']}' is not a valid operation")

    if not mutate:
        obj = deepcopy(obj)

    root = obj
    keys = op.get("path", "").split("/")
    key = None  # declare here so it can be used outside loop
    for i in range(1, len(keys)):
        key = keys[i]
        if key.find("~") != -1:
            key = unescape_json_ptr(key)
        if isinstance(obj, list):
            if key == "-":
                key = len(obj)
            else:
                key = int(key)
        if i != len(keys) - 1:
            obj = obj[key]

    if isinstance(obj, list):
        if op["op"] == "add":
            if len(obj) < key:
                # needed because insert puts at end
                # negative checked by str.isdigit()
                raise IndexError("Index out of bounds")
            obj.insert(key, op["value"])
            return ApplyResult(obj=root)
        if op["op"] == "remove":
            removed = obj[key]
            obj.pop(key)
            return ApplyResult(obj=root, removed=removed)
        if op["op"] == "replace":
            removed = obj[key]
            obj[key] = op["value"]
            return ApplyResult(obj=root, removed=removed)
        if op["op"] == "move":
            to_move = apply_operation(root, dict(op="remove", path=op["from"])).removed
            apply_operation(root, dict(op="add", path=op["path"], value=to_move))
            return ApplyResult(obj=root)
        if op["op"] == "copy":
            to_copy = get_by_ptr(root, op["from"]).obj
            apply_operation(root, dict(op="add", path=op["path"], value=deepcopy(to_copy)))
            return ApplyResult(obj=root)
        if op["op"] == "test":
            if obj[key] != op["value"]:
                raise AssertionError("Test operation failed")
            return ApplyResult(obj=root)
        if op["op"] == "_get":
            return ApplyResult(obj=obj[key] if key < len(obj) else None)
        raise ValueError(f"'{op['op']}' is not a valid operation")

    if isinstance(obj, dict):
        if op["op"] == "add":
            obj[key] = op["value"]
            return ApplyResult(obj=root)
        if op["op"] == "remove":
            removed = obj[key]
            del obj[key]
            return ApplyResult(obj=root, removed=removed)
        if op["op"] == "replace":
            removed = obj[key]
            obj[key] = op["value"]
            return ApplyResult(obj=root, removed=removed)
        if op["op"] == "move":
            to_move = apply_operation(root, dict(op="remove", path=op["from"])).removed
            apply_operation(root, dict(op="add", path=op["path"], value=to_move))
            return ApplyResult(obj=root)
        if op["op"] == "copy":
            to_copy = get_by_ptr(root, op["from"]).obj
            apply_operation(root, dict(op="add", path=op["path"], value=deepcopy(to_copy)))
            return ApplyResult(obj=root)
        if op["op"] == "test":
            if obj[key] != op["value"]:
                raise AssertionError("Test operation failed")
            return ApplyResult(obj=root)
        if op["op"] == "_get":
            return ApplyResult(obj=obj.get(key))
        raise ValueError(f"'{op['op']}' is not a valid operation")

    raise ValueError("Invalid path")


def apply_patch(obj, patch, *, mutate=True):
    """
    Applies a JSON patch on an object, based on RFC 6902 (https://datatracker.ietf.org/doc/html/rfc6902).

    :param obj: The Python object, representing a JSON
    :param patch: The patch to apply
    :param mutate: If `True`, the object will be mutated if possible. If `False`, the object never be mutated.
    :return: An `ApplyResult` with the root of the result and a list of removed objects per operation
    """

    res = ApplyResult(obj=obj)
    removed = []

    for op in patch:
        res = apply_operation(res.obj, op, mutate=mutate)
        removed.append(res.removed)

    res.removed = removed

    return res
