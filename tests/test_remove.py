import unittest

from tests.PatchTest import PatchTest, remove


class RemoveInDict(PatchTest):
    def test_in_root(self):
        self.assertPatch(
            {"foo": 1, "bar": [1, 2, 3, 4]},
            {"foo": 1},
            [remove("/bar")],
            [1, 2, 3, 4],
            ignore_patch=True,
        )

    def test_in_nested(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"qux": "hello"}]},
            {"foo": 1, "baz": [{}]},
            [remove("/baz/0/qux")],
            "hello",
            ignore_patch=True,
        )

    def test_none(self):
        self.assertPatch({"foo": None}, {}, [remove("/foo")], None, ignore_patch=True)


class RemoveInList(PatchTest):
    def test_in_root(self):
        self.assertPatch([1, 2, 3, 4], [2, 3, 4], [remove("/0")], 1, ignore_patch=True)

    def test_in_nested(self):
        self.assertPatch(
            [1, [2, 3], [4, 5, 6], [7, 8, 9, 10]],
            [1, [2, 3], [4, 6], [7, 8, 9, 10]],
            [remove("/2/1")],
            5,
            ignore_patch=True,
        )

    def test_multiple(self):
        self.assertPatch(
            [1, 2, 3, 4],
            [1, 3],
            [remove("/1"), remove("/2")],
            [2, 4],
            ignore_patch=True,
            wrap_removed=False,
        )


class RemoveRoot(PatchTest):
    def test_value(self):
        self.assertPatch(1, None, [remove("")], 1, ignore_patch=True)

    def test_dict(self):
        self.assertPatch({"foo": 1}, None, [remove("")], {"foo": 1}, ignore_patch=True)

    def test_list(self):
        self.assertPatch([1], None, [remove("")], [1], ignore_patch=True)


if __name__ == "__main__":
    unittest.main()
