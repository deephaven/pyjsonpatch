from copy import deepcopy
from typing import Any

from .types import Operation
from .utils import escape_json_ptr


def generate_patch(source: Any, target: Any) -> list[Operation]:
    """
    Creates a JSON patch from source to target, based on RFC 6902 (https://datatracker.ietf.org/doc/html/rfc6902).

    For arrays, the function will prioritize speed of comparison over the size of patch. This means that it will not
    check for remove/move operations in the middle of the array, but rather compare it index by index.

    :param source: The source Python object, representing a JSON
    :param target: The target Python object, representing a JSON
    :return: A list of operations that transforms source into target
    """

    patch: list[Operation] = []

    def _generate(source_: Any, target_: Any, path: str):
        if source_ == target_:
            return

        if isinstance(source_, dict) and isinstance(target_, dict):
            target_keys = set(target_.keys())

            for key in source_:
                if key in target_keys:
                    _generate(source_[key], target_[key], f"{path}/{escape_json_ptr(key)}")
                    target_keys.remove(key)
                else:
                    patch.append({"op": "remove", "path": f"{path}/{escape_json_ptr(key)}"})

            for key in target_keys:
                patch.append(
                    {
                        "op": "add",
                        "path": f"{path}/{escape_json_ptr(key)}",
                        "value": deepcopy(target_[key]),
                    }
                )

        elif isinstance(source_, list) and isinstance(target_, list):
            # Prioritize speed of comparison over the size of patch (do not check for remove/move in middle of list)
            smaller = source_ if len(source_) < len(target_) else target_
            for i in range(len(smaller)):
                _generate(source_[i], target_[i], f"{path}/{i}")
            if smaller is source_:
                for i in range(len(source_), len(target_)):
                    patch.append(
                        {
                            "op": "add",
                            "path": f"{path}/{i}",
                            "value": deepcopy(target_[i]),
                        }
                    )
            else:
                for i in range(len(target_), len(source_)):
                    patch.append({"op": "remove", "path": f"{path}/{i}"})

        else:
            patch.append({"op": "replace", "path": path, "value": target_})

    _generate(source, target, "")

    return patch
