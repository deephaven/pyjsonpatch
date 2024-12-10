import unittest

from tests.PatchTest import PatchTest, replace


class ReplaceInDict(PatchTest):
    def test_value_to_none(self):
        self.assertPatch({"foo": 1}, {"foo": None}, [replace("/foo", None)], 1)

    def test_none_to_value(self):
        self.assertPatch({"foo": None}, {"foo": 1}, [replace("/foo", 1)], None)

    def test_true_to_false(self):
        self.assertPatch({"foo": True}, {"foo": False}, [replace("/foo", False)], True)

    def test_false_to_true(self):
        self.assertPatch({"foo": False}, {"foo": True}, [replace("/foo", True)], False)

    def test_list_to_dict(self):
        self.assertPatch({"foo": [1]}, {"foo": {"bar": 1}}, [replace("/foo", {"bar": 1})], [1])

    def test_dict_to_list(self):
        self.assertPatch({"foo": {"bar": 1}}, {"foo": [1]}, [replace("/foo", [1])], {"bar": 1})


class ReplaceInList(PatchTest):
    def test_value_to_none(self):
        self.assertPatch([1], [None], [replace("/0", None)], 1)

    def test_none_to_value(self):
        self.assertPatch([None], [1], [replace("/0", 1)], None)

    def test_true_to_false(self):
        self.assertPatch([True], [False], [replace("/0", False)], True)

    def test_false_to_true(self):
        self.assertPatch([False], [True], [replace("/0", True)], False)

    def test_list_to_dict(self):
        self.assertPatch([[1]], [{"foo": 1}], [replace("/0", {"foo": 1})], [1])

    def test_dict_to_list(self):
        self.assertPatch([{"foo": 1}], [[1]], [replace("/0", [1])], {"foo": 1})

    def test_nested_list(self):
        # Check that it isn't being flattened
        self.assertPatch([1, 2, 3], [1, [[4], 5], 3], [replace("/1", [[4], 5])], 2)


class ReplaceInRoot(PatchTest):
    def test_value_to_none(self):
        self.assertPatch(1, None, [replace("", None)], 1, ignore_patch=True)

    def test_none_to_value(self):
        self.assertPatch(None, 1, [replace("", 1)], None, ignore_patch=True)

    def test_true_to_false(self):
        self.assertPatch(True, False, [replace("", False)], True, ignore_patch=True)

    def test_false_to_true(self):
        self.assertPatch(False, True, [replace("", True)], False, ignore_patch=True)

    def test_list_to_dict(self):
        self.assertPatch([1], {"foo": 1}, [replace("", {"foo": 1})], [1])

    def test_dict_to_list(self):
        self.assertPatch({"foo": 1}, [1], [replace("", [1])], {"foo": 1})


if __name__ == "__main__":
    unittest.main()
