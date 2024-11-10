from httpx import AsyncClient, Response
from pydantic import BaseModel

from typing import Callable, Any, Tuple, Dict


Endpoint = Callable[[
    AsyncClient, 
    BaseModel | None, 
    Tuple[Any, ...] | None, 
    Dict[str, Any] | None
], Response]
