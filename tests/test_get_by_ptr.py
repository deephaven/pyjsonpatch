import unittest

from tests.BaseTest import BaseTest


class GetByPtr(BaseTest):
    def test_root(self):
        self.assertGetByPtr({"foo": "bar", "": "world"}, "", {"foo": "bar", "": "world"})

    def test_empty_key(self):
        self.assertGetByPtr({"foo": "bar", "": "world"}, "/", "world")

    def test_nested_dict(self):
        self.assertGetByPtr({"foo": {"bar": "hello"}}, "/foo/bar", "hello")

    def test_nested_list(self):
        self.assertGetByPtr(
            {"foo": [{"bar": "hello"}, {"bar": "world"}]},
            "/foo/1/bar",
            "world")


if __name__ == "__main__":
    unittest.main()
