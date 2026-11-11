from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import SUPER_ADMIN_IDS
from database.models import Admin

ROLES = {
    "super": "👑 مدیر کل",
    "requests": "💰 مدیر درخواست‌ها",
    "support": "🎧 مدیر پشتیبانی",
    "content": "📝 مدیر محتوا",
    "users": "👥 مدیر کاربران",
}

PERMS: dict[str, set[str]] = {
    "super": {"*"},
    "requests": {"requests"},
    "support": {"tickets"},
    "content": {"gifts", "texts", "appearance", "channels", "broadcast"},
    "users": {"users"},
}


def can(admin: Admin | None, perm: str) -> bool:
    if admin is None:
        return False
    perms = PERMS.get(admin.role, set())
    return "*" in perms or perm in perms


async def get_admin(session: AsyncSession, user_id: int) -> Admin | None:
    admin = await session.get(Admin, user_id)
    if admin is None and user_id in SUPER_ADMIN_IDS:
        admin = Admin(user_id=user_id, role="super")
        session.add(admin)
        await session.flush()
    return admin
