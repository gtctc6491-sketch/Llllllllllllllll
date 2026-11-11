import asyncio
import json
import logging
from datetime import datetime
from decimal import Decimal

from aiogram import Bot
from aiogram.types import BufferedInputFile
from sqlalchemy import select

from bot.services.settings import cfg
from database.models import Admin, Base, utcnow
from database.session import async_session

log = logging.getLogger(__name__)


def _ser(v):
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


async def build_backup() -> tuple[bytes, str]:
    data: dict[str, list] = {}
    async with async_session() as s:
        for table in Base.metadata.sorted_tables:
            rows = (await s.execute(select(table))).mappings().all()
            data[table.name] = [{k: _ser(v) for k, v in r.items()} for r in rows]
    payload = {"app": "LBank-Buyer", "version": 1, "created_at": utcnow().isoformat(), "tables": data}
    raw = json.dumps(payload, ensure_ascii=False, indent=1).encode("utf-8")
    name = f"lbank_backup_{utcnow().strftime('%Y%m%d_%H%M')}.json"
    return raw, name


async def send_backup(bot: Bot, chat_id: int) -> None:
    raw, name = await build_backup()
    await bot.send_document(chat_id, BufferedInputFile(raw, filename=name), caption="💾 پشتیبان دیتابیس", parse_mode=None)


async def backup_loop(bot: Bot) -> None:
    """Periodically sends a JSON backup to every super admin."""
    await asyncio.sleep(120)
    while True:
        hours = max(1, cfg.int("backup_interval_hours"))
        if cfg.bool("backup_enabled"):
            try:
                async with async_session() as s:
                    ids = (await s.execute(select(Admin.user_id).where(Admin.role == "super"))).scalars().all()
                for uid in ids:
                    try:
                        await send_backup(bot, uid)
                    except Exception as e:
                        log.warning("backup to %s failed: %s", uid, e)
            except Exception:
                log.exception("backup loop error")
        await asyncio.sleep(hours * 3600)
