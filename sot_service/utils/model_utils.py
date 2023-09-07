from typing import Any


def dict_to_model(pkg: dict, type: Any) -> Any:
    obj = type()
    for key, val in pkg.items():
        setattr(obj, key, val)
    return obj
