import os

from dotenv import load_dotenv

load_dotenv()


def _normalize_db_url(url: str) -> str:
    """Railway/Heroku style URLs -> SQLAlchemy asyncpg URL."""
    if url.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://"):]
    return url


def _ids(raw: str) -> list[int]:
    out = []
    for part in raw.replace(" ", "").split(","):
        if part.lstrip("-").isdigit():
            out.append(int(part))
    return out


BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
DATABASE_URL: str = _normalize_db_url(
    os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./lbank_buyer.db").strip()
)
SUPER_ADMIN_IDS: list[int] = _ids(os.getenv("ADMIN_IDS", ""))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
