from sqlalchemy import select

from config.settings import SUPER_ADMIN_IDS
from database.models import Admin, BotSetting, BotText
from database.session import async_session
from utils.defaults import DEFAULT_SETTINGS, DEFAULT_TEXTS


async def seed_defaults() -> None:
    """Insert any missing default texts/settings and env super-admins (never overwrites edits)."""
    async with async_session() as s:
        have_texts = set((await s.execute(select(BotText.key))).scalars())
        for key, (_cat, _title, value, _vars) in DEFAULT_TEXTS.items():
            if key not in have_texts:
                s.add(BotText(key=key, value=value, entities="[]"))

        have_settings = set((await s.execute(select(BotSetting.key))).scalars())
        for key, value in DEFAULT_SETTINGS.items():
            if key not in have_settings:
                s.add(BotSetting(key=key, value=value))

        have_admins = set((await s.execute(select(Admin.user_id))).scalars())
        for uid in SUPER_ADMIN_IDS:
            if uid not in have_admins:
                s.add(Admin(user_id=uid, role="super"))
        await s.commit()
