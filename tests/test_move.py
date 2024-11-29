import unittest

from tests.BaseTest import BaseTest, move


class MoveInDict(BaseTest):
    def test_value(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"hello": "world"}]},
            [move("/foo", "/bar")],
            {"baz": [{"hello": "world"}], "bar": 1},
            strict_patch=False)

    def test_none(self):
        self.assertPatch(
            {"foo": None},
            [move("/foo", "/bar")],
            {"bar": None},
            strict_patch=False)

    def test_same_location(self):
        self.assertPatch(
            {"foo": 1},
            [move("/foo", "/foo")],
            {"foo": 1},
            1,
            strict_patch=False)

    def test_dict_to_list(self):
        self.assertPatch(
            {"baz": [{"qux": "hello"}], "bar": 1},
            [move("/baz/0/qux", "/baz/1")],
            {"baz": [{}, "hello"], "bar": 1},
            strict_patch=False)


class MoveReplacesRoot(BaseTest):
    def test_dict_to_dict(self):
        self.assertPatch(
            {"child": {"foo": 1}},
            [move("/child", "")],
            {"foo": 1},
            {"child": {"foo": 1}},
            strict_patch=False)

    def test_dict_to_list(self):
        self.assertPatch(
            {"child": [1]},
            [move("/child", "")],
            [1],
            {"child": [1]},
            strict_patch=False)

    def test_list_to_dict(self):
        self.assertPatch(
            ["hello", {"foo": 1}],
            [move("/1", "")],
            {"foo": 1},
            ["hello", {"foo": 1}],
            strict_patch=False)

    def test_list_to_list(self):
        self.assertPatch(
            ["hello", [1]],
            [move("/1", "")],
            [1],
            ["hello", [1]],
            strict_patch=False)


if __name__ == "__main__":
    unittest.main()
