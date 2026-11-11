"""Rendering of editable texts: dynamic variables + Telegram message entities (incl. custom emoji)."""
import json
import re

from aiogram.types import MessageEntity

VAR_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*(?::[A-Za-z0-9_]+)?)\}")


def u16len(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2


def slice_u16(text: str, offset: int, length: int) -> str:
    raw = text.encode("utf-16-le")
    return raw[offset * 2:(offset + length) * 2].decode("utf-16-le", errors="ignore")


def entities_to_json(entities) -> str:
    if not entities:
        return "[]"
    return json.dumps([e.model_dump(exclude_none=True, mode="json") for e in entities], ensure_ascii=False)


def entities_from_json(raw: str | None) -> list[MessageEntity]:
    try:
        data = json.loads(raw or "[]")
    except (TypeError, ValueError):
        return []
    out = []
    for item in data:
        try:
            out.append(MessageEntity(**item))
        except Exception:
            continue
    return out


def render(text: str, entities: list[MessageEntity], variables: dict, emojis: dict, use_premium: bool):
    """Replace {vars} and {e:name} placeholders and re-map entity offsets (UTF-16)."""
    parts: list[str] = []
    repl: list[tuple[int, int, int]] = []  # (old_start, old_end, delta)
    extra: list[MessageEntity] = []
    last = 0
    old16 = 0
    new16 = 0
    for m in VAR_RE.finditer(text):
        seg = text[last:m.start()]
        parts.append(seg)
        n = u16len(seg)
        old16 += n
        new16 += n
        raw = m.group(0)
        name = m.group(1)
        raw16 = u16len(raw)
        rep = raw
        if name.startswith("e:"):
            info = emojis.get(name[2:])
            if info:
                rep = info.get("fallback") or "⭐"
                if use_premium and info.get("id"):
                    extra.append(MessageEntity(
                        type="custom_emoji", offset=new16, length=u16len(rep),
                        custom_emoji_id=str(info["id"]),
                    ))
        elif name in variables:
            rep = str(variables[name])
        parts.append(rep)
        r16 = u16len(rep)
        repl.append((old16, old16 + raw16, r16 - raw16))
        old16 += raw16
        new16 += r16
        last = m.end()
    parts.append(text[last:])
    result = "".join(parts)

    out: list[MessageEntity] = []
    for e in entities or []:
        if e.type == "custom_emoji" and not use_premium:
            continue
        start = e.offset
        end = e.offset + e.length
        ns = start + sum(d for (_s, oe, d) in repl if oe <= start)
        ne = end + sum(d for (_s, oe, d) in repl if oe <= end)
        if ne <= ns:
            continue
        out.append(e.model_copy(update={"offset": ns, "length": ne - ns}))
    out.extend(extra)
    out.sort(key=lambda x: x.offset)
    return result, out
