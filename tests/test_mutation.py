import unittest
from copy import deepcopy

from pyjsonpatch import apply_patch
from tests.PatchTest import PatchTest, add


class MutationOn(PatchTest):
    def test_change_root(self):
        # Should mutate anyways because root went from dict to list
        obj = {"foo": 1}
        original = deepcopy(obj)
        res = apply_patch(obj, [add("", [1])])

        self.assertEqual(obj, original)
        self.assertIsNot(obj, res.obj)

    def test_change_children(self):
        obj = {"foo": 1}
        original = deepcopy(obj)
        res = apply_patch(obj, [add("/bar", 2)])

        self.assertNotEqual(obj, original)
        self.assertIs(obj, res.obj)


class MutationOff(PatchTest):
    def test_change_root(self):
        obj = {"foo": 1}
        original = deepcopy(obj)
        res = apply_patch(obj, [add("", [1])], mutate=False)

        self.assertEqual(obj, original)
        self.assertIsNot(obj, res.obj)

    def test_change_children(self):
        obj = {"foo": 1}
        original = deepcopy(obj)
        res = apply_patch(obj, [add("/bar", 2)], mutate=False)

        self.assertEqual(obj, original)
        self.assertIsNot(obj, res.obj)


if __name__ == "__main__":
    unittest.main()
