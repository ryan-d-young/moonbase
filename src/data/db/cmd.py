from datetime import datetime
from typing import Any, Tuple

import asyncpg

from data.db import sql


async def init(conn: asyncpg.Connection):
    await conn.execute(sql.SCHEMA)


async def create_table(
        conn: asyncpg.Connection,
        table: str,
        columns: Tuple[Tuple[str, str]]
):
    columns = ", ".join(f"{name} {dtype}" for name, dtype in columns)
    query = sql.CREATE_TABLE.format(table=table, columns=columns)
    await conn.execute(query)


async def insert_records(
        conn: asyncpg.Connection,
        table: str,
        columns: Tuple[str],
        values: Tuple[Tuple[Any]]
):
    columns = ", ".join(columns)
    query = sql.INSERT_RECORDS.format(table=table, columns=columns)
    await conn.executemany(query, values)


async def select_records(
        conn: asyncpg.Connection,
        table: str,
        entity: int | None = None,
        attribute: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None
):
    conditions, params = sql.conditions(entity, attribute, start_date, end_date)
    query = sql.SELECT_RECORDS.format(table=table, conditions=conditions)
    return await conn.fetch(query, *params)


async def add_provider(conn: asyncpg.Connection, name: str):
    query = sql.INSERT_RECORDS.format(
        table="_providers", 
        columns=("name",), 
        values=((name,),)
    )
    await conn.execute(query)


async def add_resource(conn: asyncpg.Connection, name: str, provider_id: int):
    query = sql.INSERT_RECORDS.format(
        table="_resources", 
        columns=("name", "provider_id"), 
        values=((name, provider_id),)
    )
    await conn.execute(query)


async def add_entity(conn: asyncpg.Connection, name: str, resource_id: int):
    query = sql.INSERT_RECORDS.format(
        table="_entities", 
        columns=("name", "resource_id"), 
        values=((name, resource_id),)
    )
    await conn.execute(query)


async def add_attribute(conn: asyncpg.Connection, name: str, entity_id: int):
    query = sql.INSERT_RECORDS.format(
        table="_attributes", 
        columns=("name", "entity_id"), 
        values=((name, entity_id),)
    )
    await conn.execute(query)


async def add_schedule(conn: asyncpg.Connection, attribute_id: int, start_date: datetime, end_date: datetime, frequency: str):
    query = sql.INSERT_RECORDS.format(
        table="_schedule", 
        columns=("attribute_id", "start_date", "end_date", "frequency"), 
        values=((attribute_id, start_date, end_date, frequency),)
    )
    await conn.execute(query)
