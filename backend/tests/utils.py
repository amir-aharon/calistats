from typing import TypeVar


T = TypeVar("T")


def soft_compare(obj1: T, obj2: T, exclude: str = "id") -> bool:
    """Compare objects of the same type, ignoring the 'id' attribute"""
    if type(obj1) is not type(obj2):
        return False

    obj1_attrs = vars(obj1)
    obj2_attrs = vars(obj2)

    for key in obj1_attrs:
        if key != exclude:
            if obj1_attrs[key] != obj2_attrs.get(key):
                return False
    return True
