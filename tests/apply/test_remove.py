import unittest

from tests.BaseTest import BaseTest, remove


class RemoveInDict(BaseTest):
    def test_in_root(self):
        self.assertPatch(
            {"foo": 1, "bar": [1, 2, 3, 4]},
            [remove("/bar")],
            {"foo": 1},
            [1, 2, 3, 4])

    def test_in_nested(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"qux": "hello"}]},
            [remove("/baz/0/qux")],
            {"foo": 1, "baz": [{}]},
            "hello")

    def test_none(self):
        self.assertPatch(
            {"foo": None},
            [remove("/foo")],
            {},
            None)


class RemoveInList(BaseTest):
    def test_in_root(self):
        self.assertPatch(
            [1, 2, 3, 4],
            [remove("/0")],
            [2, 3, 4],
            1)

    def test_in_nested(self):
        self.assertPatch(
            [1, [2, 3], [4, 5, 6], [7, 8, 9, 10]],
            [remove("/2/1")],
            [1, [2, 3], [4, 6], [7, 8, 9, 10]],
            5)

    def test_multiple(self):
        self.assertPatch(
            [1, 2, 3, 4],
            [remove("/1"), remove("/2")],
            [1, 3],
            [2, 4],
            raw_removed=True)


class RemoveRoot(BaseTest):
    def test_value(self):
        self.assertPatch(1, [remove("")], None, 1)

    def test_dict(self):
        self.assertPatch({"foo": 1}, [remove("")], None, {"foo": 1})

    def test_list(self):
        self.assertPatch([1], [remove("")], None, [1])


if __name__ == "__main__":
    unittest.main()
