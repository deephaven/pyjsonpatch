import unittest

from tests.BaseTest import BaseTest, replace


class ReplaceInDict(BaseTest):
    def test_value_to_none(self):
        self.assertPatch({"foo": 1}, [replace("/foo", None)], {"foo": None}, 1)

    def test_none_to_value(self):
        self.assertPatch({"foo": None}, [replace("/foo", 1)], {"foo": 1}, None)

    def test_true_to_false(self):
        self.assertPatch({"foo": True}, [replace("/foo", False)], {"foo": False}, True)

    def test_false_to_true(self):
        self.assertPatch({"foo": False}, [replace("/foo", True)], {"foo": True}, False)

    def test_list_to_dict(self):
        self.assertPatch({"foo": [1]}, [replace("/foo", {"bar": 1})], {"foo": {"bar": 1}}, [1])

    def test_dict_to_list(self):
        self.assertPatch({"foo": {"bar": 1}}, [replace("/foo", [1])], {"foo": [1]}, {"bar": 1})


class ReplaceInList(BaseTest):
    def test_value_to_none(self):
        self.assertPatch([1], [replace("/0", None)], [None], 1)

    def test_none_to_value(self):
        self.assertPatch([None], [replace("/0", 1)], [1], None)

    def test_true_to_false(self):
        self.assertPatch([True], [replace("/0", False)], [False], True)

    def test_false_to_true(self):
        self.assertPatch([False], [replace("/0", True)], [True], False)

    def test_list_to_dict(self):
        self.assertPatch([[1]], [replace("/0", {"foo": 1})], [{"foo": 1}], [1])

    def test_dict_to_list(self):
        self.assertPatch([{"foo": 1}], [replace("/0", [1])], [[1]], {"foo": 1})

    def test_nested_list(self):
        # Check that it isn't being flattened
        self.assertPatch([1, 2, 3], [replace("/1", [[4], 5])], [1, [[4], 5], 3], 2)


class ReplaceInRoot(BaseTest):
    def test_value_to_none(self):
        self.assertPatch(1, [replace("", None)], None, 1, strict_patch=False)

    def test_none_to_value(self):
        self.assertPatch(None, [replace("", 1)], 1, None, strict_patch=False)

    def test_true_to_false(self):
        self.assertPatch(True, [replace("", False)], False, True, strict_patch=False)

    def test_false_to_true(self):
        self.assertPatch(False, [replace("", True)], True, False, strict_patch=False)

    def test_list_to_dict(self):
        self.assertPatch([1], [replace("", {"foo": 1})], {"foo": 1}, [1])

    def test_dict_to_list(self):
        self.assertPatch({"foo": 1}, [replace("", [1])], [1], {"foo": 1})


if __name__ == "__main__":
    unittest.main()
