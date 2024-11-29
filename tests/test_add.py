import unittest
from email.policy import strict

from tests.BaseTest import BaseTest, add


class AddInDict(BaseTest):
    def test_empty_key(self):
        self.assertPatch({}, [add("/", 1)], {"": 1})

    def test_value_index(self):
        self.assertPatch({"foo": 1}, [add("/0", "bar")], {"foo": 1, "0": "bar"})

    def test_value_casing(self):
        self.assertPatch({"foo": "bar"}, [add("/FOO", "BAR")], {"foo": "bar", "FOO": "BAR"})

    def test_value_true(self):
        self.assertPatch({"foo": 1}, [add("/bar", True)], {"foo": 1, "bar": True})

    def test_value_false(self):
        self.assertPatch({"foo": 1}, [add("/bar", False)], {"foo": 1, "bar": False})

    def test_value_none(self):
        self.assertPatch({"foo": 1}, [add("/bar", None)], {"foo": 1, "bar": None})

    def test_nested_dict(self):
        self.assertPatch({"foo": {}}, [add("/foo/", 1)], {"foo": {"": 1}})

    def test_add_a_composite(self):
        self.assertPatch(
            {"foo": 1},
            [add("/bar", [1, 2])],
            {"foo": 1, "bar": [1, 2]})

    def test_add_to_composite(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"qux": "hello"}]},
            [add("/baz/0/foo", "world")],
            {"foo": 1, "baz": [{"qux": "hello", "foo": "world"}]})


class AddInList(BaseTest):
    def test_size_0_append(self):
        self.assertPatch([], [add("/-", "foo")], ["foo"], strict_patch=False)

    def test_size_0_insert_0(self):
        self.assertPatch([], [add("/0", "foo")], ["foo"])

    def test_size_2_append(self):
        self.assertPatch(
            [None, "foo"],
            [add("/-", "bar")],
            [None, "foo", "bar"],
            strict_patch=False)

    def test_size_2_insert_0(self):
        self.assertPatch(
            [None, "foo"],
            [add("/0", "bar")],
            ["bar", None, "foo"],
            strict_patch=False)

    def test_size_2_insert_1(self):
        self.assertPatch(
            [None, "foo"],
            [add("/1", "bar")],
            [None, "bar", "foo"],
            strict_patch=False)

    def test_size_2_insert_2(self):
        self.assertPatch(
            [None, "foo"],
            [add("/2", "bar")],
            [None, "foo", "bar"])

    def test_nested_insert(self):
        self.assertPatch(
            ["foo", "bar"],
            [add("/1", ["hello", "world"])],
            ["foo", ["hello", "world"], "bar"],
            strict_patch=False)

    def test_nested_append_0(self):
        self.assertPatch(
            [1, 2],
            [add("/-", {"foo": ["bar", "baz"]})],
            [1, 2, {"foo": ["bar", "baz"]}],
            strict_patch=False)

    def test_nested_append_1(self):
        self.assertPatch(
            [1, 2, [3, [4, 5]]],
            [add("/2/1/-", {"foo": ["bar", "baz"]})],
            [1, 2, [3, [4, 5, {"foo": ["bar", "baz"]}]]],
            strict_patch=False)


class AddReplacesInDict(BaseTest):
    def test_value_to_none(self):
        self.assertPatch(
            {"foo": 1},
            [add("/foo", None)],
            {"foo": None},
            strict_patch=False)

    def test_none_to_value(self):
        self.assertPatch(
            {"foo": None},
            [add("/foo", 1)],
            {"foo": 1},
            strict_patch=False)

    def test_true_to_false(self):
        self.assertPatch(
            {"foo": True},
            [add("/foo", False)],
            {"foo": False},
            strict_patch=False)

    def test_false_to_true(self):
        self.assertPatch(
            {"foo": False},
            [add("/foo", True)],
            {"foo": True},
            strict_patch=False)

    def test_list_to_dict(self):
        self.assertPatch(
            {"foo": [1]},
            [add("/foo", {"bar": 1})],
            {"foo": {"bar": 1}},
            strict_patch=False)

    def test_dict_to_list(self):
        self.assertPatch(
            {"foo": {"bar": 1}},
            [add("/foo", [1])],
            {"foo": [1]},
            strict_patch=False)


class AddReplacesInRoot(BaseTest):
    def test_value_to_none(self):
        self.assertApply(1, [add("", None)], None)

    def test_none_to_value(self):
        self.assertApply(None, [add("", 1)], 1)

    def test_true_to_false(self):
        self.assertApply(True, [add("", False)], False)

    def test_false_to_true(self):
        self.assertApply(False, [add("", True)], True)

    def test_list_to_dict(self):
        self.assertApply([1], [add("", {"foo": 1})], {"foo": 1})

    def test_dict_to_list(self):
        self.assertApply({"foo": 1}, [add("", [1])], [1])


if __name__ == "__main__":
    unittest.main()
