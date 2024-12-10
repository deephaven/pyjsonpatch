import unittest

from tests.PatchTest import PatchTest


# From https://datatracker.ietf.org/doc/html/rfc6901#section-5
class PointerSpec(PatchTest):
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
        self.assertGetByPointer(doc, "", doc)
        self.assertGetByPointer(doc, "/foo", ["bar", "baz"])
        self.assertGetByPointer(doc, "/foo/0", "bar")
        self.assertGetByPointer(doc, "/", 0)
        self.assertGetByPointer(doc, "/a~1b", 1)
        self.assertGetByPointer(doc, "/c%d", 2)
        self.assertGetByPointer(doc, "/e^f", 3)
        self.assertGetByPointer(doc, "/g|h", 4)
        self.assertGetByPointer(doc, "/i\\j", 5)
        self.assertGetByPointer(doc, '/k"l', 6)
        self.assertGetByPointer(doc, "/ ", 7)
        self.assertGetByPointer(doc, "/m~0n", 8)


# From https://datatracker.ietf.org/doc/html/rfc6902#appendix-A
class PatchSpec(PatchTest):
    def test_a1(self):
        self.assertPatch(
            {"foo": "bar"},
            {"baz": "qux", "foo": "bar"},
            [{"op": "add", "path": "/baz", "value": "qux"}],
        )

    def test_a2(self):
        self.assertPatch(
            {"foo": ["bar", "baz"]},
            {"foo": ["bar", "qux", "baz"]},
            [{"op": "add", "path": "/foo/1", "value": "qux"}],
            ignore_patch=True,
        )

    def test_a3(self):
        self.assertPatch(
            {"baz": "qux", "foo": "bar"}, {"foo": "bar"}, [{"op": "remove", "path": "/baz"}], "qux"
        )

    def test_a4(self):
        self.assertPatch(
            {"foo": ["bar", "qux", "baz"]},
            {"foo": ["bar", "baz"]},
            [{"op": "remove", "path": "/foo/1"}],
            "qux",
            ignore_patch=True,
        )

    def test_a5(self):
        self.assertPatch(
            {"baz": "qux", "foo": "bar"},
            {"baz": "boo", "foo": "bar"},
            [{"op": "replace", "path": "/baz", "value": "boo"}],
            "qux",
        )

    def test_a6(self):
        self.assertPatch(
            {"foo": {"bar": "baz", "waldo": "fred"}, "qux": {"corge": "grault"}},
            {"foo": {"bar": "baz"}, "qux": {"corge": "grault", "thud": "fred"}},
            [{"op": "move", "from": "/foo/waldo", "path": "/qux/thud"}],
            ignore_patch=True,
        )

    def test_a7(self):
        self.assertPatch(
            {"foo": ["all", "grass", "cows", "eat"]},
            {"foo": ["all", "cows", "eat", "grass"]},
            [{"op": "move", "from": "/foo/1", "path": "/foo/3"}],
            ignore_patch=True,
        )

    def test_a8(self):
        self.assertPatch(
            {"baz": "qux", "foo": ["a", 2, "c"]},
            {"baz": "qux", "foo": ["a", 2, "c"]},
            [
                {"op": "test", "path": "/baz", "value": "qux"},
                {"op": "test", "path": "/foo/1", "value": 2},
            ],
            ignore_patch=True,
        )

    def test_a9(self):
        self.assertApplyRaises(
            {"baz": "qux"},
            [{"op": "test", "path": "/baz", "value": "bar"}],
            AssertionError("Test operation failed"),
        )

    def test_a10(self):
        self.assertPatch(
            {"foo": "bar"},
            {"foo": "bar", "child": {"grandchild": {}}},
            [{"op": "add", "path": "/child", "value": {"grandchild": {}}}],
            ignore_patch=True,
        )

    def test_a11(self):
        self.assertPatch(
            {"foo": "bar"},
            {"foo": "bar", "baz": "qux"},
            [{"op": "add", "path": "/baz", "value": "qux", "xyz": 123}],
            ignore_patch=True,
        )

    def test_a12(self):
        self.assertApplyRaises(
            {"foo": "bar"}, [{"op": "add", "path": "/baz/bat", "value": "qux"}], KeyError("baz")
        )

    # Test A13 skipped because it checks the JSON spec instead of JSON Patch

    def test_a14(self):
        self.assertPatch(
            {"/": 9, "~1": 10},
            {"/": 9, "~1": 10},
            [{"op": "test", "path": "/~01", "value": 10}],
            ignore_patch=True,
        )

    def test_a15(self):
        self.assertApplyRaises(
            {"/": 9, "~1": 10},
            [{"op": "test", "path": "/~01", "value": "10"}],
            AssertionError("Test operation failed"),
        )

    def test_a16(self):
        self.assertPatch(
            {"foo": ["bar"]},
            {"foo": ["bar", ["abc", "def"]]},
            [{"op": "add", "path": "/foo/-", "value": ["abc", "def"]}],
            ignore_patch=True,
        )


if __name__ == "__main__":
    unittest.main()
