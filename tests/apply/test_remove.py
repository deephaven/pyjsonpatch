import unittest

from tests.BaseTest import BaseTest


class RemoveDict(BaseTest):
    def test_in_root(self):
        self.assertPatch(
            {"foo": 1, "bar": [1, 2, 3, 4]},
            [{"op": "remove", "path": "/bar"}],
            {"foo": 1})

    def test_in_nested(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"qux": "hello"}]},
            [{"op": "remove", "path": "/baz/0/qux"}],
            {"foo": 1, "baz": [{}]})

    def test_none(self):
        self.assertPatch(
            {"foo": None},
            [{"op": "remove", "path": "/foo"}],
            {})


class RemoveList(BaseTest):
    def test_in_root(self):
        self.assertPatch(
            [1, 2, 3, 4],
            [{"op": "remove", "path": "/0"}],
            [2, 3, 4])

    def test_in_nested(self):
        self.assertPatch(
            [1, [2, 3], [4, 5, 6], [7, 8, 9, 10]],
            [{"op": "remove", "path": "/2/1"}],
            [1, [2, 3], [4, 6], [7, 8, 9, 10]])

    def test_multiple(self):
        self.assertPatch(
            [1, 2, 3, 4],
            [{"op": "remove", "path": "/1"}, {"op": "remove", "path": "/2"}],
            [1, 3])



if __name__ == "__main__":
    unittest.main()
