from __future__ import annotations

from copy import deepcopy
from typing import Any
from unittest import TestCase

from pyjsonpatch import Operation, apply_patch, generate_patch, get_by_ptr


class PatchTest(TestCase):
    def assertGetByPtr(self, obj: Any, ptr: str, expect: Any):
        """
        Asserts that getting a value by pointer from an object is successful.

        :param obj: The object to get from
        :param ptr: The pointer to get
        :param expect: The expected result
        """

        self.assertEqual(get_by_ptr(obj, ptr).obj, expect)
        self.assertEqual(apply_patch(obj, [dict(op="_get", path=ptr)]).obj, expect)

    def assertApply(
        self,
        obj: Any,
        patch: list[Operation],
        expect: Any,
        removed: Any = None,
        *,
        ignore_removed=False,
        wrap_removed=True,
    ):
        """
        Asserts a patch operation is successful.

        If `wrap_removed` is `True`, `removed` will be wrapped in a list. If it is `None`, it will be replaced with a
        list of `None`s (same size of patch).

        :param obj: The original object
        :param patch: The patch to apply
        :param expect: The expected result object
        :param removed: The expected removed object
        :param ignore_removed: Do not check removed
        :param wrap_removed: Wrap removed with rules from above
        """

        res = apply_patch(obj, patch)
        self.assertEqual(res.obj, expect)

        if wrap_removed:
            if removed is None:
                removed = [None] * len(patch)
            else:
                removed = [removed]

        if not ignore_removed:
            self.assertListEqual(res.removed, removed)

    def assertApplyRaises(self, obj: Any, patch: list[Operation], err: Exception):
        """
        Asserts that applying a patch raises the given exception.

        :param obj: The original object
        :param patch: The patch to apply
        :param err: The expected exception
        """

        with self.assertRaises(type(err)) as e:
            apply_patch(obj, patch)

        self.assertTupleEqual(e.exception.args, err.args)

    def assertGenerate(self, obj1: Any, obj2: Any, patch: list[Operation], *, ignore_patch=True):
        """
        Asserts that a patch generated from `obj1` and `obj2` is the same as the given patch.

        :param obj1: The original object
        :param obj2: The result object
        :param patch: The patch to expect
        :param ignore_patch: Do not check patch
        """

        res = generate_patch(obj1, obj2)
        if not ignore_patch:
            self.assertListEqual(res, patch)

        self.assertApply(obj1, res, obj2, ignore_removed=True)

    def assertPatch(
        self,
        obj1: Any,
        obj2: Any,
        patch: list[Operation],
        removed: Any = None,
        *,
        ignore_patch=False,
        ignore_removed=False,
        wrap_removed=True,
    ):
        """
        Asserts that :
         - The patch applied to `obj1` results in `obj2`
         - The patch generated from `obj1` and `obj2`:
           - Is the same as the given patch if `ignore_patch` is False
           - Applied to `obj1` results in `obj2`

        If `wrap_removed` is `True`, `removed` will be wrapped in a list. If it is `None`, it will be replaced with a
        list of `None`s (same size of patch).

        :param obj1: The original object
        :param obj2: The expected result object
        :param patch: The patch to apply, and expected from generate
        :param removed: The expected removed object
        :param ignore_patch: Do not check patch for generate
        :param ignore_removed: Do not check removed for apply
        :param wrap_removed: Wrap removed with rules from above
        """

        obj1_ = deepcopy(obj1)
        obj2_ = deepcopy(obj2)
        self.assertGenerate(obj1, obj2, patch, ignore_patch=ignore_patch)
        self.assertApply(
            obj1_,
            patch,
            obj2_,
            removed,
            ignore_removed=ignore_removed,
            wrap_removed=wrap_removed,
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
