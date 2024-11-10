import pydantic
from typing import Callable
from collections import defaultdict

from data.rest.common import Endpoint


_REGISTRY: dict[str, dict[str, dict[str, Endpoint | pydantic.BaseModel | None]]] = defaultdict(dict)


def _register(provider: str, endpoint: str, resource: str, fn: Callable, model: pydantic.BaseModel | None = None):
    _REGISTRY[provider][endpoint] = {"resource": resource, "fn": fn, "model": model}


def get(provider: str, endpoint: str) -> dict[str, Callable | pydantic.BaseModel | None] | None:
    return _REGISTRY[provider].get(endpoint)


def register(resource: str, schema: dict | None = None):
    def decorator(func):
        _register(
            provider=__name__, endpoint=func.__name__, 
            resource=resource, fn=func, 
            model=pydantic.create_model(
                f"{__name__}.{func.__name__}", **schema
            ) if schema else None
        )
        return func
    return decorator
