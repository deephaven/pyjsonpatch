import unittest

from tests.PatchTest import PatchTest, add, copy


class CopyReplacesRoot(PatchTest):
    def test_dict_to_dict(self):
        self.assertPatch({"child": {"foo": 1}}, {"foo": 1}, [copy("/child", "")], ignore_patch=True)

    def test_dict_to_list(self):
        self.assertPatch({"child": [1]}, [1], [copy("/child", "")], ignore_patch=True)

    def test_list_to_dict(self):
        self.assertPatch(["hello", {"foo": 1}], {"foo": 1}, [copy("/1", "")], ignore_patch=True)

    def test_list_to_list(self):
        self.assertPatch(["hello", [1]], [1], [copy("/1", "")], ignore_patch=True)


class CopyValues(PatchTest):
    def test_none(self):
        self.assertPatch(
            {"foo": None},
            {"foo": None, "bar": None},
            [copy("/foo", "/bar")],
            ignore_patch=True,
        )

    def test_list(self):
        self.assertPatch(
            {"baz": ["hello", "world"], "bar": 1},
            {"baz": ["hello", "world"], "bar": 1, "boo": ["hello", "world"]},
            [copy("/baz", "/boo")],
            ignore_patch=True,
        )

    def test_dict(self):
        self.assertPatch(
            {"baz": {"hello": "world"}, "bar": 1},
            {"baz": {"hello": "world"}, "bar": 1, "boo": {"hello": "world"}},
            [copy("/baz", "/boo")],
            ignore_patch=True,
        )

    def test_no_list_cross_reference(self):
        self.assertPatch(
            {"foo": [1, 2, [3]]},
            {"foo": [1, 2, [3]], "copy": [1, 2, [3, 4]]},
            [copy("/foo", "/copy"), add("/copy/2/-", 4)],
            ignore_patch=True,
        )

    def test_no_dict_cross_reference(self):
        self.assertPatch(
            {"foo": {"bar": {"hello": 1}}},
            {"foo": {"bar": {"hello": 1}}, "copy": {"bar": {"hello": 1, "world": 2}}},
            [copy("/foo", "/copy"), add("/copy/bar/world", 2)],
            ignore_patch=True,
        )


if __name__ == "__main__":
    unittest.main()
