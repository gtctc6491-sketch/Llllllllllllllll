import time
from collections import defaultdict, deque

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.messaging import send_key
from bot.services.perms import get_admin
from bot.services.settings import cfg
from bot.services.subscription import get_missing, send_sub_required
from bot.services.texts import T
from database.models import User, utcnow


class AccessMiddleware(BaseMiddleware):
    """User registration, block check, anti-spam and mandatory-channel gate."""

    def __init__(self) -> None:
        self.hits: dict[int, deque] = defaultdict(deque)
        self.last_warn: dict[int, float] = {}

    async def _upsert(self, session: AsyncSession, tg) -> User:
        user = await session.get(User, tg.id)
        if user is None:
            user = User(id=tg.id, username=tg.username, first_name=tg.first_name or "", last_name=tg.last_name)
            session.add(user)
            await session.flush()
            return user
        if user.username != tg.username:
            user.username = tg.username
        if user.first_name != (tg.first_name or ""):
            user.first_name = tg.first_name or ""
        if user.last_name != tg.last_name:
            user.last_name = tg.last_name
        if (utcnow() - user.last_seen).total_seconds() > 60:
            user.last_seen = utcnow()
        return user

    def _throttled(self, uid: int) -> bool:
        now = time.monotonic()
        window = max(1, cfg.int("rate_limit_window"))
        limit = max(3, cfg.int("rate_limit_events"))
        dq = self.hits[uid]
        while dq and now - dq[0] > window:
            dq.popleft()
        if len(dq) >= limit:
            return True
        dq.append(now)
        return False

    async def __call__(self, handler, event, data):
        tg = data.get("event_from_user")
        if tg is None or tg.is_bot:
            return None
        if isinstance(event, Message):
            chat = event.chat
        elif isinstance(event, CallbackQuery) and event.message:
            chat = event.message.chat
        else:
            chat = None
        if chat is not None and chat.type != "private":
            return None

        session: AsyncSession = data["session"]
        bot = data["bot"]
        user = await self._upsert(session, tg)
        admin = await get_admin(session, tg.id)
        data["db_user"] = user
        data["admin"] = admin
        data["is_admin"] = admin is not None
        if admin is not None:
            return await handler(event, data)

        if user.is_blocked:
            if isinstance(event, CallbackQuery):
                await event.answer(T.plain("blocked", tg), show_alert=True)
            else:
                await send_key(bot, tg.id, "blocked", None, tg)
            return None

        if self._throttled(tg.id):
            now = time.monotonic()
            if now - self.last_warn.get(tg.id, 0) > cfg.int("rate_limit_window"):
                self.last_warn[tg.id] = now
                if isinstance(event, CallbackQuery):
                    await event.answer(T.plain("rate_limited", tg), show_alert=True)
                else:
                    await send_key(bot, tg.id, "rate_limited", None, tg)
            elif isinstance(event, CallbackQuery):
                await event.answer()
            return None

        is_start = isinstance(event, Message) and (event.text or "").startswith("/start")
        is_check = isinstance(event, CallbackQuery) and event.data == "check_sub"
        if not (is_start or is_check):
            missing = await get_missing(bot, session, tg.id)
            if missing:
                if isinstance(event, CallbackQuery):
                    await event.answer()
                await send_sub_required(event, missing)
                return None
        return await handler(event, data)
