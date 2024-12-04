from __future__ import annotations

from copy import deepcopy
from typing import Any
from unittest import TestCase

from pyjsonpatch import Operation, apply_patch, generate_patch, get_by_ptr


class BaseTest(TestCase):
    def assertApply(
        self,
        obj: Any,
        patch: list[Operation],
        expect: Any,
        removed: Any = None,
        *,
        ignore_removed=False,
        raw_removed=False,
    ):
        """
        Asserts a patch operation is successful.

        IF `raw_removed` is False, `removed` will be wrapped in a list if it's defined, or replaced with a list
        of Nones (same size of patch). This is done because most tests are a single operation, and it makes it
        more readable if there's no extra wrapping.

        :param obj: The original object
        :param patch: The patch to apply
        :param expect: The expected result object
        :param removed: The expected removed object
        :param ignore_removed: Do not check removed
        :param raw_removed: Do not wrap removed
        """

        res = apply_patch(obj, patch)
        self.assertEqual(res.obj, expect)

        if not raw_removed:
            if removed is None:
                removed = [None] * len(patch)
            else:
                removed = [removed]
        if not ignore_removed:
            self.assertListEqual(res.removed, removed)

    def assertPatchRaises(self, obj: Any, patch: list[Operation], err: Exception):
        with self.assertRaises(type(err)) as e:
            apply_patch(obj, patch)

        self.assertTupleEqual(e.exception.args, err.args)

    def assertGetByPtr(self, obj: Any, ptr: str, expect: Any):
        self.assertEqual(get_by_ptr(obj, ptr).obj, expect)
        self.assertEqual(apply_patch(obj, [dict(op="_get", path=ptr)]).obj, expect)

    def assertGenerate(self, obj1: Any, obj2: Any, patch: list[Operation], *, strict_patch=True):
        res = generate_patch(obj1, obj2)
        if strict_patch:
            self.assertListEqual(res, patch)
        self.assertApply(obj1, patch, obj2, ignore_removed=True)

    def assertPatch(
        self,
        obj1: Any,
        patch: list[Operation],
        obj2: Any,
        removed: Any = None,
        *,
        ignore_removed=False,
        raw_removed=False,
        strict_patch=True,
    ):
        """
        Asserts that:
         - A patch applied to obj1 results in obj2
         - A patch generated from obj1 and obj2 is the same as the given patch

        If `raw_removed` is False, `removed` will be modified with the following rules
         - If `removed` is None, it will be replaced with a list of Nones (same size of patch)
         - Else, it will be wrapped in a list

        :param obj1: The original object
        :param obj2: The expected result object
        :param patch: The patch to apply
        :param removed: The expected removed object
        :param ignore_removed: Do not check removed
        :param raw_removed: If removed should not be modified
        """

        obj1_ = deepcopy(obj1)
        obj2_ = deepcopy(obj2)
        self.assertGenerate(obj1, obj2, patch, strict_patch=strict_patch)
        self.assertApply(
            obj1_,
            patch,
            obj2_,
            removed,
            ignore_removed=ignore_removed,
            raw_removed=raw_removed,
        )


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
