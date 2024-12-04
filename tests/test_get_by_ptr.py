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
        self.assertGetByPtr({"foo": [{"bar": "hello"}, {"bar": "world"}]}, "/foo/1/bar", "world")

    def test_spec(self):
        doc = {
            "foo": ["bar", "baz"],
            "": 0,
            "a/b": 1,
            "c%d": 2,
            "e^f": 3,
            "g|h": 4,
            "i\\j": 5,
            'k"l': 6,
            " ": 7,
            "m~n": 8,
        }
        self.assertGetByPtr(doc, "", doc)
        self.assertGetByPtr(doc, "/foo", ["bar", "baz"])
        self.assertGetByPtr(doc, "/foo/0", "bar")
        self.assertGetByPtr(doc, "/", 0)
        self.assertGetByPtr(doc, "/a~1b", 1)
        self.assertGetByPtr(doc, "/c%d", 2)
        self.assertGetByPtr(doc, "/e^f", 3)
        self.assertGetByPtr(doc, "/g|h", 4)
        self.assertGetByPtr(doc, "/i\\j", 5)
        self.assertGetByPtr(doc, '/k"l', 6)
        self.assertGetByPtr(doc, "/ ", 7)
        self.assertGetByPtr(doc, "/m~0n", 8)


if __name__ == "__main__":
    unittest.main()
