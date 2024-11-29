import unittest

from tests.BaseTest import BaseTest, add, copy


class CopyReplacesRoot(BaseTest):
    def test_dict_to_dict(self):
        self.assertPatch(
            {"child": {"foo": 1}},
            [copy("/child", "")],
            {"foo": 1},
            strict_patch=False)

    def test_dict_to_list(self):
        self.assertPatch(
            {"child": [1]},
            [copy("/child", "")],
            [1],
            strict_patch=False)

    def test_list_to_dict(self):
        self.assertPatch(
            ["hello", {"foo": 1}],
            [copy("/1", "")],
            {"foo": 1},
            strict_patch=False)

    def test_list_to_list(self):
        self.assertPatch(
            ["hello", [1]],
            [copy("/1", "")],
            [1],
            strict_patch=False)


class CopyValues(BaseTest):
    def test_none(self):
        self.assertPatch(
            {"foo": None},
            [copy("/foo", "/bar")],
            {"foo": None, "bar": None},
            strict_patch=False)

    def test_list(self):
        self.assertPatch(
            {"baz": ["hello", "world"], "bar": 1},
            [copy("/baz", "/boo")],
            {"baz": ["hello", "world"], "bar": 1, "boo": ["hello", "world"]},
            strict_patch=False)

    def test_dict(self):
        self.assertPatch(
            {"baz": {"hello": "world"}, "bar": 1},
            [copy("/baz", "/boo")],
            {"baz": {"hello": "world"}, "bar": 1, "boo": {"hello": "world"}},
            strict_patch=False)

    def test_no_list_cross_reference(self):
        self.assertPatch(
            {"foo": [1, 2, [3]]},
            [copy("/foo", "/copy"), add("/copy/2/-", 4)],
            {"foo": [1, 2, [3]], "copy": [1, 2, [3, 4]]},
            strict_patch=False)

    def test_no_dict_cross_reference(self):
        self.assertPatch(
            {"foo": {"bar": {"hello": 1}}},
            [copy("/foo", "/copy"), add("/copy/bar/world", 2)],
            {"foo": {"bar": {"hello": 1}}, "copy": {"bar": {"hello": 1, "world": 2}}},
            strict_patch=False)


if __name__ == "__main__":
    unittest.main()
