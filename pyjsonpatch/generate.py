from copy import deepcopy
from typing import Any

from .utils import escape_json_ptr


def _get_keys(obj: list | dict) -> list[Any]:
    if isinstance(obj, list):
        return list(range(len(obj)))
    elif isinstance(obj, dict):
        return list(obj.keys())


def _has_key(obj: list | dict, key: int | str) -> bool:
    if isinstance(obj, dict):
        return key in obj
    elif isinstance(obj, list) and type(key) is int:
        return 0 <= key < len(obj)
    return False


def generate_patch(obj1, obj2):
    patches = []

    def _generate(old: list | dict, new: list | dict, path):
        if old == new:
            return

        new_keys = _get_keys(new)
        old_keys = _get_keys(old)
        deleted = False

        for key in reversed(old_keys):
            old_val = old[key]

            if _has_key(new, key) and not (new[key] is None and old_val is not None and not isinstance(new, list)):
                new_val = new[key]
                if isinstance(old_val, dict) and isinstance(new_val, dict) and isinstance(old_val, list) == isinstance(new_val, list):
                    _generate(old_val, new_val, f"{path}/{escape_json_ptr(str(key))}")
                elif old_val != new_val:
                    patches.append({"op": "replace", "path": f"{path}/{escape_json_ptr(str(key))}", "value": deepcopy(new_val)})

            elif isinstance(old, list) and isinstance(new, list):
                patches.append({"op": "remove", "path": f"{path}/{escape_json_ptr(str(key))}"})
                deleted = True

            else:
                patches.append({"op": "replace", "path": path, "value": new})

        if not deleted and len(new_keys) == len(old_keys):
            return

        for key in new_keys:
            if not _has_key(old, key) and new[key] is not None:
                patches.append({'op': 'add', 'path': f"{path}/{escape_json_ptr(str(key))}", 'value': deepcopy(new[key])})


    _generate(obj1, obj2, "")

    return patches
