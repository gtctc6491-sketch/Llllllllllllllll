from aiogram import BaseMiddleware

from database.session import async_session


class DbSessionMiddleware(BaseMiddleware):
    """One DB session per update; commit on success, rollback on error."""

    async def __call__(self, handler, event, data):
        async with async_session() as session:
            data["session"] = session
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
