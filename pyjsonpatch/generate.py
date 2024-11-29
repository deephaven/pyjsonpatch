from copy import deepcopy
from typing import Any

from .utils import escape_json_ptr


def _get_keys(obj: list | dict) -> list[Any]:
    if isinstance(obj, list):
        return list(range(len(obj)))
    elif isinstance(obj, dict):
        return list(obj.keys())
    return []


def _get_value(obj: list | dict, key: int | str) -> Any:
    if isinstance(obj, dict):
        return obj.get(key)
    elif isinstance(obj, list) and type(key) is int:
        return obj[key] if 0 <= key < len(obj) else None
    return None


def _has_key(obj: list | dict, key: int | str) -> bool:
    if isinstance(obj, dict):
        return key in obj
    elif isinstance(obj, list) and type(key) is int:
        return 0 <= key < len(obj)
    return False


def generate_patch(obj1, obj2):
    patches = []

    def _generate(mirror: list | dict, obj: list | dict, path):
        if mirror == obj:
            return

        new_keys = _get_keys(obj)
        old_keys = _get_keys(mirror)
        deleted = False

        for key in reversed(old_keys):
            old_val = _get_value(mirror, key)

            if _has_key(obj, key) and not (key not in obj and key in mirror and not isinstance(obj, list)):
                new_val = _get_value(obj, key)
                if isinstance(old_val, (dict, list)) and isinstance(new_val, (dict, list)) and isinstance(old_val, list) == isinstance(new_val, list):
                    _generate(old_val, new_val, f"{path}/{escape_json_ptr(str(key))}")
                elif old_val != new_val:
                    patches.append({"op": "replace", "path": f"{path}/{escape_json_ptr(str(key))}", "value": deepcopy(new_val)})

            elif isinstance(mirror, list) == isinstance(obj, list):
                patches.append({"op": "remove", "path": f"{path}/{escape_json_ptr(str(key))}"})
                deleted = True

            else:
                patches.append({"op": "replace", "path": path, "value": obj})

        if not deleted and len(new_keys) == len(old_keys):
            return

        for key in new_keys:
            if not _has_key(mirror, key) and _has_key(obj, key):
                patches.append({'op': 'add', 'path': f"{path}/{escape_json_ptr(str(key))}", 'value': deepcopy(obj[key])})

    _generate(obj1, obj2, "")

    return patches
