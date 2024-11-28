from typing import Any
from unittest import TestCase

from pyjsonpatch import apply_patch, Operation, get_by_ptr


class BaseTest(TestCase):
    def assertPatch(self, obj: Any, patch: list[Operation], expect: Any, removed: Any = None, *,
                    raw_removed = False):
        """
        Asserts a patch operation is successful.

        IF `raw_removed` is False, `removed` will be wrapped in a list if it's defined, or replaced with a list
        of Nones (same size of patch). This is done because most tests are a single operation, and it makes it
        more readable if there's not extra wrapping.

        :param obj: The original object
        :param patch: The patch to apply
        :param expect: The expected result object
        :param removed: The expected removed object
        :param raw_removed: Do not wrap removed
        :return:
        """

        res = apply_patch(obj, patch)
        self.assertEqual(res.obj, expect)

        if not raw_removed:
            if removed is None:
                removed = [None] * len(patch)
            else:
                removed = [removed]
        self.assertListEqual(res.removed, removed)

    def assertPatchRaises(self, obj: Any, patch: list[Operation], err: Exception):
        with self.assertRaises(type(err)) as e:
            apply_patch(obj, patch)

        self.assertTupleEqual(e.exception.args, err.args)

    def assertGetByPtr(self, obj: Any, ptr: str, expect: Any):
        self.assertEqual(get_by_ptr(obj, ptr).obj, expect)
        self.assertEqual(apply_patch(obj, [dict(op="_get", path=ptr)]).obj, expect)


def add(path="", value=""):
    return {"op": "add", "path": path, "value": value}


def move(from_="", path=""):
    return {"op": "move", "from": from_, "path": path}


def copy(from_="", path=""):
    return {"op": "copy", "from": from_, "path": path}


def remove(path=""):
    return {"op": "remove", "path": path}


def replace(path="", value=""):
    return {"op": "replace", "path": path, "value": value}
