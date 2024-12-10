import unittest

from tests.PatchTest import PatchTest, move


class MoveInDict(PatchTest):
    def test_value(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"hello": "world"}]},
            {"baz": [{"hello": "world"}], "bar": 1},
            [move("/foo", "/bar")],
            ignore_patch=True,
        )

    def test_none(self):
        self.assertPatch({"foo": None}, {"bar": None}, [move("/foo", "/bar")], ignore_patch=True)

    def test_same_location(self):
        self.assertPatch({"foo": 1}, {"foo": 1}, [move("/foo", "/foo")], ignore_patch=True)

    def test_dict_to_list(self):
        self.assertPatch(
            {"baz": [{"qux": "hello"}], "bar": 1},
            {"baz": [{}, "hello"], "bar": 1},
            [move("/baz/0/qux", "/baz/1")],
            ignore_patch=True,
        )


class MoveInList(PatchTest):
    def test_index_0_2(self):
        self.assertPatch([1, 2, 3, 4, 5], [2, 3, 1, 4, 5], [move("/0", "/2")], ignore_patch=True)

    def test_index_2_0(self):
        self.assertPatch([1, 2, 3, 4, 5], [3, 1, 2, 4, 5], [move("/2", "/0")], ignore_patch=True)

    def test_index_0_0(self):
        self.assertPatch([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [move("/0", "/0")], ignore_patch=True)

    def test_index_2_2(self):
        self.assertPatch([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [move("/2", "/2")], ignore_patch=True)

    def test_to_end(self):
        self.assertPatch([1, 2, 3, 4, 5], [1, 2, 4, 5, 3], [move("/2", "/-")], ignore_patch=True)


class MoveReplacesRoot(PatchTest):
    def test_dict_to_dict(self):
        self.assertPatch({"child": {"foo": 1}}, {"foo": 1}, [move("/child", "")], ignore_patch=True)

    def test_dict_to_list(self):
        self.assertPatch({"child": [1]}, [1], [move("/child", "")], ignore_patch=True)

    def test_list_to_dict(self):
        self.assertPatch(["hello", {"foo": 1}], {"foo": 1}, [move("/1", "")], ignore_patch=True)

    def test_list_to_list(self):
        self.assertPatch(["hello", [1]], [1], [move("/1", "")], ignore_patch=True)


if __name__ == "__main__":
    unittest.main()
