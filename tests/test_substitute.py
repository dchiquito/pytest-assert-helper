from pytest_deep.substitute import Any, Type, Re, Id, Timestamp


def test_any():
    assert Any() == 1
    assert 1 == Any()
    assert Any() == "string"
    assert "string" == Any()
    assert Any() == []
    assert [] == Any()
    assert Any() == [1, 2, 3]
    assert [1, 2, 3] == Any()
    assert Any() == {}
    assert {} == Any()
    assert Any() == {1: 2}
    assert {1: 2} == Any()


def test_type():
    assert Type(str) == "123"
    assert Type(str) != 123
    assert Type(int) == 123
    assert Type(int) != "123"
    assert Type(list) == []
    assert Type(list) != {}
    assert Type(dict) == {}
    assert Type(dict) != []
    assert Type(object) == "123"
    assert Type(object) == 123
    assert Type(object) == []
    assert Type(object) == {}


def test_re():
    assert Re("") == ""
    assert Re("abc") == "abc"
    assert Re("[a-b]") == "a"
    assert Re("[a-b]") == "b"
    assert Re("[a-b]") != "ab"
    assert Re("[a-b]") != "c"


def test_id():
    assert Id() == "123456789012345678901234"
    assert Id() != "gggggggggggggggggggggggg"
    assert Id() != "123"
    assert Id() != ""


def test_timestamp():
    assert Timestamp() == "2020-03-19T18:59:56.416611+00:00"
    assert Timestamp() != ""


def test_substitute_permanence():
    x = Any()
    assert x == 1
    assert x != 2

    y = Any()
    assert 1 == y
    assert 2 != y
    assert x == y

    z = Any()
    assert {
        "key1": z,
        "key2": [z, 6, 7],
        "key3": z,
        "key4": {"A significantly long string": {4: z}},
    } == {
        "key1": 5,
        "key2": [5, 6, 7],
        "key3": 5,
        "key4": {"A significantly long string": {4: 5}},
    }
