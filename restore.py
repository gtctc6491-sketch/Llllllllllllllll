"""Restore a JSON backup created by the bot into an EMPTY database.

Usage:  python -m utils.restore lbank_backup_YYYYMMDD_HHMM.json
"""
import asyncio
import json
import sys
from datetime import datetime

from sqlalchemy import DateTime, text

from database.models import Base
from database.session import engine, init_db


def _convert(table, row: dict) -> dict:
    out = {}
    for col in table.columns:
        v = row.get(col.name)
        if v is not None and isinstance(col.type, DateTime):
            v = datetime.fromisoformat(v)
        out[col.name] = v
    return out


async def restore(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    await init_db()
    async with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            rows = payload.get("tables", {}).get(table.name, [])
            if rows:
                await conn.execute(table.insert(), [_convert(table, r) for r in rows])
                print(f"{table.name}: {len(rows)} rows")
        if engine.dialect.name == "postgresql":
            for table in Base.metadata.sorted_tables:
                if "id" in table.c and table.c.id.autoincrement is not False and table.c.id.primary_key \
                        and table.c.id.type.python_type is int and table.name not in ("users",):
                    await conn.execute(text(
                        f"SELECT setval(pg_get_serial_sequence('{table.name}', 'id'), "
                        f"COALESCE((SELECT MAX(id) FROM {table.name}), 1))"))
    print("✅ restore finished")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m utils.restore <backup.json>")
    asyncio.run(restore(sys.argv[1]))
