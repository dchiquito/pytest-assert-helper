import re

from pytest_deep.substitute import Any, Type, Re
from pytest_deep.deep_list import List
from pytest_deep.deep_dict import Dict

# Old tests, will go away soon


def test_lists():
    assert List([]) == []
    assert List([1, "2", {"t": []}]) == [1, "2", {"t": []}]
    assert List([1, Any(), 3]) == [1, 2, 3]
    assert List([1]) != []
    assert List([]) != [1]
    # Lists with allow_extra
    assert List(allow_extra=True) == [1, 2, 3]
    assert List([], allow_extra=True) == [1, 2, 3]
    assert List([1, 2], allow_extra=True) == [1, 2, 3]
    assert List([1, 2, 3], allow_extra=True) == [1, 2, 3]
    assert List([1, 2, 3, 4], allow_extra=True) != [1, 2, 3]
    # Lists with ignore_order
    assert List([], ignore_order=True) == []
    assert List(["1"], ignore_order=True) == ["1"]
    assert List(["1", "2"], ignore_order=True) == ["1", "2"]
    assert List(["1", "2"], ignore_order=True) == ["2", "1"]
    assert List(["1", "2", 3], ignore_order=True) != ["2", "1"]
    # Lists with allow_extra and ignore_order
    assert List(allow_extra=True, ignore_order=True) == []
    assert List([], allow_extra=True, ignore_order=True) == []
    assert List([], allow_extra=True, ignore_order=True) == [1, "z", str, {7: [8, "9"]}]
    assert List([666], allow_extra=True, ignore_order=True) != [
        1,
        "z",
        str,
        {7: [8, "9"]},
    ]


def test_dicts():
    assert Dict({}) == {}
    assert Dict({1: "2", "3": [4], 5: None}) == {1: "2", "3": [4], 5: None}
    assert Dict({1: "2", "3": [4]}) != {1: "2", "3": [4, 5]}
    assert Dict({1: 2}) != {1: 2, 3: 4}
    # Dicts with More
    assert Dict({More(): Any()}) == {1: 2, 3: 4}
    assert Dict({More(): Any(), 3: 4}) == {1: 2, 3: 4}
    assert Dict({More(): Any(), 5: 4}) != {1: 2, 3: 4}
    assert Dict({More(): Type(int)}) == {1: 2, 3: 4}
    assert Dict({More(): Type(int), 3: 4}) == {1: 2, 3: 4}
    assert Dict({More(): Type(int), 3: 4}) != {1: "2", 3: 4}
    assert Dict({More(): Type(int), 5: 4}) != {1: 2, 3: 4}


def test_everything():
    assert List(
        [
            Dict(
                {
                    "name": "Daniel",
                    "fav_type": str,
                    "created": Type(str),
                    More(): Type(int),
                }
            ),
            Dict(
                {
                    "name": "Chiquito",
                    "fav_type": Any(),
                    "created": "January",
                    "address": Re("[0-9]+ ([A-Z][a-z]+ ?)+"),
                }
            ),
            More(),
            AnyOrder(),
        ]
    ) == [
        {
            "name": "Chiquito",
            "fav_type": int,
            "created": "January",
            "address": "101 East Weaver Street",
        },
        "lol",
        {
            "name": "Daniel",
            "fav_type": str,
            "created": "February",
            "age": 42,
            "fav_number": 42,
        },
    ]
