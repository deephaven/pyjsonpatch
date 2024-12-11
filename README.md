# pyjsonpatch

![GitHub License](https://img.shields.io/github/license/deephaven/pyjsonpatch)
![GitHub branch check runs](https://img.shields.io/github/check-runs/deephaven/pyjsonpatch/main)


## About

A Python implementation of JSON Pointer ([RFC 6902](https://datatracker.ietf.org/doc/html/rfc6901)) and JSON Patch ([RFC 6902](https://datatracker.ietf.org/doc/html/rfc6902)). Primarily, the package can do the following to Python object(s) representing JSON(s):
- `apply_patch` to modify an object with a JSON patch
- `generate_patch` to generate a JSON Patch from two objects
- `get_by_ptr` to retrieve a value from object using a JSON pointer

## Table of Contents

- [About](#about)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Examples](#examples)
  - [`get_by_ptr`](#get_by_ptr)
  - [`apply_patch`](#apply_patch)
  - [`generate_patch`](#generate_patch)


## Installation

Python 3.8 or higher is required. You can install the library with:
```sh
# TODO
```

## Examples

### `get_by_ptr`

```python
from pyjsonpatch import get_by_ptr


source = {"": 1, "foo": [2, 3]}

print(get_by_ptr(source, "").obj)
# {"": 1, "foo": [2, 3]}
print(get_by_ptr(source, "/").obj)
# 1
print(get_by_ptr(source, "/foo").obj)
# [2, 3]
print(get_by_ptr(source, "/foo/0").obj)
# 2
```

### `apply_patch`

```python
from pyjsonpatch import apply_patch


source = {"": 1, "foo": [2, 3]}
patch = [
  {"op": "add", "path": "/hello", "value": "world"},
  {"op": "add", "path": "/foo/1", "value": 4},
  {"op": "add", "path": "/foo/-", "value": 5},
  {"op": "remove", "path": "/"},
]
res = apply_patch(source, patch)

print(res.obj)
# {"foo": [2, 4, 3, 5], "hello": "world"}
print(res.obj is source)
# True
#  - source was mutated
print(res.removed)
# [None, None, None, 1]
#  - Only the 4th operation removes something
```

### `generate_patch`

```python
from pyjsonpatch import generate_patch


source = {"": 1, "foo": [2, 3]}
target = {"foo": [2, 4], "hello": "world"}
print(generate_patch(source, target))
# [
#   {"op": "remove": "path": "/"},
#   {"op": "replace": "path": "/foo/1", "value": 4},
#   {"op": "add": "path": "/hello", "value": "world"},
# ]
```
