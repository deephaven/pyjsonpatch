from copy import deepcopy
from typing import Any

from .types import Operation, ApplyResult
from .utils import unescape_json_ptr


def _apply_dict_operation(root: Any, obj: dict, key: str, op: Operation) -> ApplyResult:
    """
    Apply an operation to a specific dict

    :param root: The root of the entire JSON
    :param obj: The parent dict to apply the operation to
    :param key: The key tp apply the operation to
    :param op: The operation
    :return: An ApplyResult of the operation
    """

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
        removed = get_by_ptr(root, op["path"])
        to_move = apply_operation(root, dict(op="remove", path=op["from"]))
        apply_operation(root, dict(op="add", path=op["path"], value=to_move))
        return ApplyResult(obj=root, removed=removed)
    if op["op"] == "copy":
        to_copy = get_by_ptr(root, op["from"])
        apply_operation(root, dict(op="add", path=op["path"], value=deepcopy(to_copy)))
        return ApplyResult(obj=root)
    if op["op"] == "test":
        return ApplyResult(obj=root, test=obj[key] == op["value"])
    if op["op"] == "_get":
        return ApplyResult(obj=root)
    raise NotImplementedError


def _apply_list_operation(root: Any, obj: list, key: int, op: Operation) -> ApplyResult:
    """
    Apply an operation to a specific list

    :param root: The root of the entire JSON
    :param obj: The parent list to apply the operation to
    :param key: The key (index) tp apply the operation to
    :param op: The operation
    :return: An ApplyResult of the operation
    """

    if op["op"] == "add":
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
        removed = get_by_ptr(root, op["path"])
        to_move = apply_operation(root, dict(op="remove", path=op["from"]))
        apply_operation(root, dict(op="add", path=op["path"], value=to_move))
        return ApplyResult(obj=root, removed=removed)
    if op["op"] == "copy":
        to_copy = get_by_ptr(root, op["from"])
        apply_operation(root, dict(op="add", path=op["path"], value=deepcopy(to_copy)))
        return ApplyResult(obj=root)
    if op["op"] == "test":
        return ApplyResult(obj=root, test=obj[key] == op["value"])
    if op["op"] == "_get":
        return ApplyResult(obj=root)


def get_by_ptr(obj: Any, ptr: str):
    if ptr == "":
        return obj
    return apply_operation(obj, {"op": "_get", "path": ptr})


def apply_operation(obj: Any, op: Operation, *, never_mutate: bool = False, validate: bool = False):
    # Root operations, will mutate root no matter what
    if op["path"] == "":
        if op["op"] == "add":
            return ApplyResult(obj=op["value"])
        if op["op"] == "remove":
            return ApplyResult(obj=None, removed=obj)
        if op["op"] == "replace":
            return ApplyResult(obj=op["value"], removed=obj)
        if op["op"] == "move" or op["op"] == "copy":
            return ApplyResult(
                obj=get_by_ptr(obj, op["from"]),
                removed=obj if op["op"] == "move" else None)
        if op["test"] == "test":
            if obj != op["value"]:
                raise AssertionError("Test operation failed")
            return ApplyResult(obj=obj)
        if op["op"] == "_get":
            return ApplyResult(obj=obj)

        if validate:
            raise Exception("invalid operation")
        return ApplyResult(obj=obj)

    if never_mutate:
        obj = deepcopy(obj)

    path = op.get("path", "")
    keys = path.split("/")
    root = obj
    existing_key = None
    i = 1

    while True:
        key = keys[i]
        if key.find("~") != -1:
            key = unescape_json_ptr(key)

        # TODO validation

        i += 1
        if isinstance(obj, list):
            if key == "-":
                key = len(obj)
            elif key.isdigit():
                key = int(key)
            else:
                if validate:
                    raise TypeError(f"Key {key} is not an integer")

            if i >= len(keys):
                if validate and op["op"] == "add" and key > len(obj):
                    raise KeyError(f"Cannot insert at key {key} of {obj}")
                ret = _apply_list_operation(root, obj, key, op)
                if ret.test is False:
                    raise AssertionError("Test operation failed")
                return ret

        elif isinstance(obj, dict):
            if i >= len(keys):
                ret = _apply_dict_operation(root, obj, key, op)
                if ret.test is False:
                    raise AssertionError("Test operation failed")
                return ret

        obj = obj[key]
        if validate and i < len(keys) and (obj is not None or not isinstance(obj, dict)):
            raise KeyError("Key not found")


def apply_patch(obj, patch):
    res = ApplyResult(obj=obj)
    for op in patch:
        res = apply_operation(res.obj, op)

    return res
