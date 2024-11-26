import unittest

from tests.BaseTest import BaseTest


class TestEmpty(BaseTest):
    def test_same_order(self):
        self.assertPatch({}, [], {})
        self.assertPatch(["foo"], [], ["foo"])
        self.assertPatch({"foo": 1}, [], {"foo": 1})

    def test_reorder_object(self):
        self.assertPatch(
            {"foo": 1, "bar": 2},
            [],
            {"bar":2, "foo": 1}
        )
        self.assertPatch(
            [{"foo": 1, "bar": 2}],
            [],
            [{"bar":2, "foo": 1}]
        )
        self.assertPatch(
            {"foo":{"foo": 1, "bar": 2}},
            [],
            {"foo":{"bar":2, "foo": 1}}
        )


if __name__ == "__main__":
    unittest.main()
