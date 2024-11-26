import unittest

from tests.BaseTest import BaseTest


class ReplaceDict(BaseTest):
    def test_root_value(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "replace", "path": "", "value": {"bar": 2}}],
            {"bar": 2})

    def test_replaces_none(self):
        self.assertPatch(
            {"foo": None},
            [{"op": "replace", "path": "", "value": {"bar": 2}}],
            {"bar": 2})

    def test_replace_with_none(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "replace", "path": "", "value": {"bar": None}}],
            {"bar": None})


class ReplaceList(BaseTest):
    def test_root_value(self):
        self.assertPatch(
            ["foo"],
            [{"op": "replace", "path": "/0", "value": "bar"}],
            ["bar"])

    def test_root_int(self):
        self.assertPatch(
            ["foo"],
            [{"op": "replace", "path": "/0", "value": 0}],
            [0])

    def test_root_true(self):
        self.assertPatch(
            ["foo"],
            [{"op": "replace", "path": "/0", "value": True}],
            [True])

    def test_root_false(self):
        self.assertPatch(
            ["foo"],
            [{"op": "replace", "path": "/0", "value": False}],
            [False])

    def test_root_none(self):
        self.assertPatch(
            ["foo"],
            [{"op": "replace", "path": "/0", "value": None}],
            [None])

    def test_nested_lists(self):
        self.assertPatch(
            ["foo", "bar"],
            [{"op": "replace", "path": "/1", "value": ["hello", "world"]}],
            ["foo", ["hello", "world"]])


if __name__ == "__main__":
    unittest.main()
