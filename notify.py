import logging

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.perms import can
from database.models import Admin

log = logging.getLogger(__name__)


async def admins_with(session: AsyncSession, perm: str) -> list[Admin]:
    rows = (await session.execute(select(Admin))).scalars().all()
    return [a for a in rows if can(a, perm)]


async def notify_admins(bot: Bot, session: AsyncSession, perm: str, text: str, markup=None) -> list[int]:
    sent = []
    for a in await admins_with(session, perm):
        try:
            await bot.send_message(a.user_id, text, reply_markup=markup, parse_mode=None)
            sent.append(a.user_id)
        except Exception as e:  # admin may not have started the bot
            log.warning("notify admin %s failed: %s", a.user_id, e)
    return sent


async def send_file(bot: Bot, chat_id: int, file_type: str | None, file_id: str, caption: str | None = None):
    if file_type == "photo":
        return await bot.send_photo(chat_id, file_id, caption=caption, parse_mode=None)
    return await bot.send_document(chat_id, file_id, caption=caption, parse_mode=None)
