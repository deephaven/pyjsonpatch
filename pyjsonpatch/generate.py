from __future__ import annotations

from copy import deepcopy
from typing import Any

from .types import Operation
from .utils import escape_json_ptr


def generate_patch(
    source: Any, target: Any, path: str = "", patch: list[Operation] | None = None
) -> list[Operation]:
    """
    Creates a JSON patch from source to target, based on RFC 6902 (https://datatracker.ietf.org/doc/html/rfc6902).

    For arrays, the function will prioritize speed of comparison over the size of patch. This means that it will not
    check for remove/move operations in the middle of the array, but rather compare it index by index.

    :param source: The source Python object, representing a JSON
    :param target: The target Python object, representing a JSON
    :param path: The current path in the JSON
    :param patch: The list of operations to append to. If not provided, a new list will be created
    :return: A list of operations that transforms source into target
    """
    if patch is None:
        patch = []

    if source is target or source == target:
        return patch

    if isinstance(source, dict) and isinstance(target, dict):
        target_keys = set(target.keys())

        for key in source:
            if key in target_keys:
                generate_patch(
                    source[key], target[key], f"{path}/{escape_json_ptr(key)}", patch
                )
                target_keys.remove(key)
            else:
                patch.append({"op": "remove", "path": f"{path}/{escape_json_ptr(key)}"})

        for key in target_keys:
            patch.append(
                {
                    "op": "add",
                    "path": f"{path}/{escape_json_ptr(key)}",
                    "value": deepcopy(target[key]),
                }
            )

    elif isinstance(source, list) and isinstance(target, list):
        # Prioritize speed of comparison over the size of patch (do not check for remove/move in middle of list)
        if len(source) < len(target):
            for i in range(len(source)):
                generate_patch(source[i], target[i], f"{path}/{i}", patch)
            for i in range(len(source), len(target)):
                patch.append(
                    {
                        "op": "add",
                        "path": f"{path}/{i}",
                        "value": deepcopy(target[i]),
                    }
                )
        else:
            for i in range(len(target)):
                generate_patch(source[i], target[i], f"{path}/{i}", patch)
            # Start from end to avoid index shifting
            for i in range(len(source) - 1, len(target) - 1, -1):
                patch.append({"op": "remove", "path": f"{path}/{i}"})

    else:
        patch.append({"op": "replace", "path": path, "value": target})

    return patch
