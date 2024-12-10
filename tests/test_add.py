import unittest

from tests.PatchTest import PatchTest, add


class AddInDict(PatchTest):
    def test_empty_key(self):
        self.assertPatch({}, {"": 1}, [add("/", 1)])

    def test_value_index(self):
        self.assertPatch({"foo": 1}, {"foo": 1, "0": "bar"}, [add("/0", "bar")])

    def test_value_casing(self):
        self.assertPatch({"foo": "bar"}, {"foo": "bar", "FOO": "BAR"}, [add("/FOO", "BAR")])

    def test_value_true(self):
        self.assertPatch({"foo": 1}, {"foo": 1, "bar": True}, [add("/bar", True)])

    def test_value_false(self):
        self.assertPatch({"foo": 1}, {"foo": 1, "bar": False}, [add("/bar", False)])

    def test_value_none(self):
        self.assertPatch({"foo": 1}, {"foo": 1, "bar": None}, [add("/bar", None)])

    def test_nested_dict(self):
        self.assertPatch({"foo": {}}, {"foo": {"": 1}}, [add("/foo/", 1)])

    def test_add_a_composite(self):
        self.assertPatch({"foo": 1}, {"foo": 1, "bar": [1, 2]}, [add("/bar", [1, 2])])

    def test_add_to_composite(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"qux": "hello"}]},
            {"foo": 1, "baz": [{"qux": "hello", "foo": "world"}]},
            [add("/baz/0/foo", "world")],
        )


class AddInList(PatchTest):
    def test_size_0_append(self):
        self.assertPatch([], ["foo"], [add("/-", "foo")], ignore_patch=True)

    def test_size_0_insert_0(self):
        self.assertPatch([], ["foo"], [add("/0", "foo")])

    def test_size_2_append(self):
        self.assertPatch([None, "foo"], [None, "foo", "bar"], [add("/-", "bar")], ignore_patch=True)

    def test_size_2_insert_0(self):
        self.assertPatch([None, "foo"], ["bar", None, "foo"], [add("/0", "bar")], ignore_patch=True)

    def test_size_2_insert_1(self):
        self.assertPatch([None, "foo"], [None, "bar", "foo"], [add("/1", "bar")], ignore_patch=True)

    def test_size_2_insert_2(self):
        self.assertPatch([None, "foo"], [None, "foo", "bar"], [add("/2", "bar")])

    def test_nested_insert(self):
        self.assertPatch(
            ["foo", "bar"],
            ["foo", ["hello", "world"], "bar"],
            [add("/1", ["hello", "world"])],
            ignore_patch=True,
        )

    def test_nested_append_0(self):
        self.assertPatch(
            [1, 2],
            [1, 2, {"foo": ["bar", "baz"]}],
            [add("/-", {"foo": ["bar", "baz"]})],
            ignore_patch=True,
        )

    def test_nested_append_1(self):
        self.assertPatch(
            [1, 2, [3, [4, 5]]],
            [1, 2, [3, [4, 5, {"foo": ["bar", "baz"]}]]],
            [add("/2/1/-", {"foo": ["bar", "baz"]})],
            ignore_patch=True,
        )


class AddReplacesInDict(PatchTest):
    def test_value_to_none(self):
        self.assertPatch({"foo": 1}, {"foo": None}, [add("/foo", None)], ignore_patch=True)

    def test_none_to_value(self):
        self.assertPatch({"foo": None}, {"foo": 1}, [add("/foo", 1)], ignore_patch=True)

    def test_true_to_false(self):
        self.assertPatch({"foo": True}, {"foo": False}, [add("/foo", False)], ignore_patch=True)

    def test_false_to_true(self):
        self.assertPatch({"foo": False}, {"foo": True}, [add("/foo", True)], ignore_patch=True)

    def test_list_to_dict(self):
        self.assertPatch(
            {"foo": [1]},
            {"foo": {"bar": 1}},
            [add("/foo", {"bar": 1})],
            ignore_patch=True,
        )

    def test_dict_to_list(self):
        self.assertPatch({"foo": {"bar": 1}}, {"foo": [1]}, [add("/foo", [1])], ignore_patch=True)


class AddReplacesInRoot(PatchTest):
    def test_value_to_none(self):
        self.assertPatch(1, None, [add("", None)], ignore_patch=True)

    def test_none_to_value(self):
        self.assertPatch(None, 1, [add("", 1)], ignore_patch=True)

    def test_true_to_false(self):
        self.assertPatch(True, False, [add("", False)], ignore_patch=True)

    def test_false_to_true(self):
        self.assertPatch(False, True, [add("", True)], ignore_patch=True)

    def test_list_to_dict(self):
        self.assertPatch([1], {"foo": 1}, [add("", {"foo": 1})], ignore_patch=True)

    def test_dict_to_list(self):
        self.assertPatch({"foo": 1}, [1], [add("", [1])], ignore_patch=True)


if __name__ == "__main__":
    unittest.main()
