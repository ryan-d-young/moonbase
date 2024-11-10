import httpx
import pydantic

import asyncio

from data.rest.common import Endpoint



def make(
        fn: Endpoint, 
        client: httpx.AsyncClient, 
        model: pydantic.BaseModel | None = None,
        *args, **kwargs
    ) -> asyncio.Task[httpx.Response]:
    if model:
        model = model(*args, **kwargs)
        return asyncio.create_task(fn(client, model))
    else:
        return asyncio.create_task(fn(client))


async def execute(task: asyncio.Task[httpx.Response]) -> httpx.Response:
    result = await task
    return result
