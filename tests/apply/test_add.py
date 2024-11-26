import unittest

from tests.BaseTest import BaseTest


class AddAsReplace(BaseTest):
    def test_replace_none(self):
        self.assertPatch(
            {"foo": None},
            [{"op": "add", "path": "/foo", "value": 1}],
            {"foo": 1})

    def test_replace_root_empty_dict(self):
        self.assertPatch(
            {},
            [{"op": "add", "path": "", "value": []}],
            [])

    def test_replace_root_empty_list(self):
        self.assertPatch(
            [],
            [{"op": "add", "path": "", "value": {}}],
            {})

    def test_replace_root_dict(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "add", "path": "", "value": {"bar": 2}}],
            {"bar": 2})


class AddDict(BaseTest):
    def test_empty_key(self):
        self.assertPatch(
            {},
            [{"op": "add", "path": "/", "value": 1}],
            {"": 1})

    def test_value_index(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "add", "path": "/0", "value": "bar"}],
            {"foo": 1, "0": "bar"})

    def test_value_capitalization(self):
        self.assertPatch(
            {"foo": "bar"},
            [{"op": "add", "path": "/FOO", "value": "BAR"}],
            {"foo": "bar", "FOO": "BAR"})

    def test_value_true(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "add", "path": "/bar", "value": True}],
            {"foo": 1, "bar": True})

    def test_value_false(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "add", "path": "/bar", "value": False}],
            {"foo": 1, "bar": False})

    def test_value_none(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "add", "path": "/bar", "value": None}],
            {"foo": 1, "bar": None})

    def test_nested_dict(self):
        self.assertPatch(
            {"foo": {}},
            [{"op": "add", "path": "/foo/", "value": 1}],
            {"foo": {"": 1}})

    def test_add_a_composite(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "add", "path": "/bar", "value": [1, 2]}],
            {"foo": 1, "bar": [1, 2]})

    def test_add_to_composite(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"qux": "hello"}]},
            [{"op": "add", "path": "/baz/0/foo", "value": "world"}],
            {"foo": 1, "baz": [{"qux": "hello", "foo": "world"}]})


class AddList(BaseTest):
    def test_size_0_append(self):
        self.assertPatch(
            [],
            [{"op": "add", "path": "/-", "value": "foo"}],
            ["foo"])

    def test_size_0_insert_0(self):
        self.assertPatch(
            [],
            [{"op": "add", "path": "/0", "value": "foo"}],
            ["foo"])

    def test_size_2_append(self):
        self.assertPatch(
            [None, "foo"],
            [{"op": "add", "path": "/-", "value": "bar"}],
            [None, "foo", "bar"])

    def test_size_2_insert_0(self):
        self.assertPatch(
            [None, "foo"],
            [{"op": "add", "path": "/0", "value": "bar"}],
            ["bar", None, "foo"])

    def test_size_2_insert_1(self):
        self.assertPatch(
            [None, "foo"],
            [{"op": "add", "path": "/1", "value": "bar"}],
            [None, "bar", "foo"])

    def test_size_2_insert_2(self):
        self.assertPatch(
            [None, "foo"],
            [{"op": "add", "path": "/2", "value": "bar"}],
            [None, "foo", "bar"])

    def test_nested_insert(self):
        self.assertPatch(
            ["foo", "bar"],
            [{"op": "add", "path": "/1", "value": ["hello", "world"]}],
            ["foo", ["hello", "world"], "bar"])

    def test_nested_append_0(self):
        self.assertPatch(
            [1, 2],
            [{"op": "add", "path": "/-", "value": {"foo": ["bar", "baz"]}}],
            [1, 2, {"foo": ["bar", "baz"]}])

    def test_nested_append_1(self):
        self.assertPatch(
            [1, 2, [3, [4, 5]]],
            [{"op": "add", "path": "/2/1/-", "value": {"foo": ["bar", "baz"]}}],
            [1, 2, [3, [4, 5, {"foo": ["bar", "baz"]}]]])



if __name__ == "__main__":
    unittest.main()
