import unittest

from tests.PatchTest import PatchTest


class GetByPointer(PatchTest):
    def test_root(self):
        self.assertGetByPointer({"foo": "bar", "": "world"}, "", {"foo": "bar", "": "world"})

    def test_empty_key(self):
        self.assertGetByPointer({"foo": "bar", "": "world"}, "/", "world")

    def test_nested_dict(self):
        self.assertGetByPointer({"foo": {"bar": "hello"}}, "/foo/bar", "hello")

    def test_nested_list(self):
        self.assertGetByPointer(
            {"foo": [{"bar": "hello"}, {"bar": "world"}]}, "/foo/1/bar", "world"
        )


if __name__ == "__main__":
    unittest.main()
