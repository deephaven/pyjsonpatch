import unittest

from tests.BaseTest import BaseTest


class Move(BaseTest):
    def test_value(self):
        self.assertPatch(
            {"foo": 1, "baz": [{"hello": "world"}]},
            [{"op": "move", "from": "/foo", "path": "/bar"}],
            {"baz": [{"hello": "world"}], "bar": 1})

    def test_none(self):
        self.assertPatch(
            {"foo": None},
            [{"op": "move", "from": "/foo", "path": "/bar"}],
            {"bar": None})

    def test_same_location(self):
        self.assertPatch(
            {"foo": 1},
            [{"op": "move", "from": "/foo", "path": "/foo"}],
            {"foo": 1})

    def test_dict_to_list(self):
        self.assertPatch(
            {"baz": [{"qux": "hello"}], "bar": 1},
            [{"op": "move", "from": "/baz/0/qux", "path": "/baz/1"}],
            {"baz": [{}, "hello"], "bar": 1})



if __name__ == "__main__":
    unittest.main()
