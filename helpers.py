import math
import re
from datetime import datetime

PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
PAGE_SIZE = 8

REQUEST_STATUS = {
    "pending": "⏳ در انتظار بررسی",
    "in_review": "🔍 در حال بررسی",
    "approved": "✅ تأیید شده",
    "rejected": "❌ رد شده",
}
REQUEST_EMOJI = {"pending": "⏳", "in_review": "🔍", "approved": "✅", "rejected": "❌"}
TICKET_STATUS = {
    "waiting": "🟡 در انتظار پاسخ",
    "answered": "🟢 پاسخ داده شد",
    "closed": "⚫️ بسته شده",
}
TICKET_EMOJI = {"waiting": "🟡", "answered": "🟢", "closed": "⚫️"}


def norm_digits(s: str) -> str:
    return (s or "").translate(PERSIAN_DIGITS)


def parse_amount(text: str) -> float | None:
    t = norm_digits(text).replace(",", "").replace("٬", "").replace("$", "")
    m = re.search(r"\d+(?:\.\d+)?", t)
    if not m:
        return None
    try:
        return float(m.group())
    except ValueError:
        return None


def parse_year(text: str) -> int | None:
    t = norm_digits(text)
    m = re.search(r"(?<!\d)(\d{4})(?!\d)", t)
    if not m:
        return None
    year = int(m.group(1))
    now = datetime.utcnow().year
    if 2000 <= year <= now + 1:
        return year
    return None


def fmt_amount(a: float) -> str:
    s = f"{a:,.2f}".rstrip("0").rstrip(".")
    return s


def fmt_dt(dt: datetime | None) -> str:
    return dt.strftime("%Y-%m-%d %H:%M") + " UTC" if dt else "—"


def page_count(total: int) -> int:
    return max(1, math.ceil(total / PAGE_SIZE))


def clamp_page(page: int, pages: int) -> int:
    return max(0, min(page, pages - 1))


def uname(username: str | None) -> str:
    return f"@{username}" if username else "—"


def full_name(first: str | None, last: str | None = None) -> str:
    return " ".join(x for x in [first or "", last or ""] if x).strip() or "—"
