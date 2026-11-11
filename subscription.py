import logging
import time

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.common import btn, ikb, tb
from bot.services.messaging import show
from database.models import MandatoryChannel

log = logging.getLogger(__name__)
_ok_until: dict[int, float] = {}
CACHE_SECONDS = 45


def forget(user_id: int) -> None:
    _ok_until.pop(user_id, None)


async def active_channels(session: AsyncSession) -> list[MandatoryChannel]:
    q = select(MandatoryChannel).where(MandatoryChannel.is_active.is_(True)).order_by(MandatoryChannel.id)
    return list((await session.execute(q)).scalars().all())


async def get_missing(bot: Bot, session: AsyncSession, user_id: int) -> list[MandatoryChannel]:
    if _ok_until.get(user_id, 0) > time.monotonic():
        return []
    missing = []
    for ch in await active_channels(session):
        try:
            m = await bot.get_chat_member(ch.chat_id, user_id)
            joined = m.status in ("creator", "administrator", "member") or (
                m.status == "restricted" and getattr(m, "is_member", False))
        except Exception as e:
            # bot not admin / channel removed: don't lock users out because of a config problem
            log.warning("membership check failed for channel %s: %s", ch.chat_id, e)
            joined = True
        if not joined:
            missing.append(ch)
    if not missing:
        _ok_until[user_id] = time.monotonic() + CACHE_SECONDS
    return missing


async def send_sub_required(event, missing: list[MandatoryChannel]):
    rows = [[btn(f"📢 {ch.title}", url=ch.link)] for ch in missing]
    rows.append([btn(tb("btn_check_sub"), "check_sub")])
    return await show(event, "sub_required", ikb(rows))
