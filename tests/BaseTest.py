from typing import Any
from unittest import TestCase

from pyjsonpatch import apply_patch, Operation


class BaseTest(TestCase):
    def assertPatch(self, src: Any, patch: list[Operation], expected: Any, msg: str | None = None):
        self.assertTrue(type(src) is dict or type(src) is list, msg)
        self.assertTrue(type(expected) is dict or type(expected) is list, msg)

        if type(expected) == dict:
            self.assertDictEqual(apply_patch(src, patch).obj, expected, msg)
        elif type(expected) == list:
            self.assertListEqual(apply_patch(src, patch).obj, expected, msg)

    def assertPatchRaises(self, src: Any, patch: list[Operation], err: Exception):
        with self.assertRaises(type(err)) as e:
            apply_patch(src, patch)

        self.assertTupleEqual(e.exception.args, err.args)
