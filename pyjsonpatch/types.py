from __future__ import annotations
from typing import TypedDict, Literal


AddOperation = TypedDict("AddOperation", {"op": Literal["add"], "path": str, "value": str})
RemoveOperation = TypedDict("RemoveOperation", {"op": Literal["remove"], "path": str})
ReplaceOperation = TypedDict("ReplaceOperation", {"op": Literal["replace"], "path": str, "value": str})
MoveOperation = TypedDict("MoveOperation", {"op": Literal["move"], "from": str, "path": str})
CopyOperation = TypedDict("CopyOperation", {"op": Literal["copy"], "from": str, "path": str})
TestOperation = TypedDict("TestOperation", {"op": Literal["test"], "path": str, "value": str})
Operation = AddOperation | RemoveOperation

class ApplyResult:
    def __init__(self, *, obj = None, removed = None, test = None):
        self.obj = obj
        self.removed = removed
        self.test = test
