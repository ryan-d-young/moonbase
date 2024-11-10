
from datetime import datetime

SCHEMA = """
CREATE SCHEMA IF NOT EXISTS raw_data;
CREATE TABLE IF NOT EXISTS raw_data._providers (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS raw_data._resources (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    provider_id INTEGER NOT NULL REFERENCES raw_data._providers(id)
);
CREATE TABLE IF NOT EXISTS raw_data._entities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    resource_id INTEGER NOT NULL REFERENCES raw_data._resources(id),
);
CREATE TABLE IF NOT EXISTS raw_data._attributes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    entity_id INTEGER NOT NULL REFERENCES raw_data._entities(id)
);
CREATE TABLE IF NOT EXISTS raw_data._schedule (
    id SERIAL PRIMARY KEY,
    attribute_id INTEGER NOT NULL REFERENCES raw_data._attributes(id),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    frequency TEXT NOT NULL
);
"""
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS raw_data.{table} (
    id SERIAL PRIMARY KEY,
    {columns}
);
"""
INSERT_RECORDS = """
INSERT INTO raw_data.{table} ({columns}) VALUES ({values});
"""
SELECT_RECORDS = """
SELECT * FROM raw_data.{table}{conditions};
"""
DROP_TABLE = """
DROP TABLE IF EXISTS raw_data.{table};
"""
DROP_SCHEMA = """
DROP SCHEMA IF EXISTS raw_data CASCADE;
"""


def conditions(
        entity: int | None = None, 
        attribute: int | None = None, 
        start_date: datetime | None = None, 
        end_date: datetime | None = None
) -> str:
    conditions = []
    params = []
    if entity:
        conditions.append("entity_id = $1")
        params.append(entity)
    if attribute:
        conditions.append(f"attribute_id = ${len(params) + 1}")
        params.append(attribute)
    if start_date:
        conditions.append(f"timestamp >= ${len(params) + 1}")
        params.append(start_date)
    if end_date:
        conditions.append(f"timestamp <= ${len(params) + 1}")
        params.append(end_date)
    if conditions:
        return "WHERE " + " AND ".join(conditions), params
    return "", []
