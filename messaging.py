"""Sending helpers: entity-aware text, safe fallbacks when custom emoji are unsupported."""
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from bot.services.texts import T
from utils.telegram_text import u16len


def _plain_ents(ents):
    return [e for e in (ents or []) if e.type != "custom_emoji"]


async def send_text(bot: Bot, chat_id: int, text: str, ents=None, markup: InlineKeyboardMarkup | None = None):
    try:
        return await bot.send_message(chat_id, text, entities=ents or None, reply_markup=markup, parse_mode=None)
    except TelegramBadRequest:
        # most common cause: custom emoji not allowed for this bot -> resend with regular emoji
        return await bot.send_message(chat_id, text, entities=_plain_ents(ents) or None, reply_markup=markup, parse_mode=None)


async def send_key(bot: Bot, chat_id: int, key: str, markup=None, user=None, **extra):
    text, ents = T.render(key, user, **extra)
    return await send_text(bot, chat_id, text, ents, markup)


async def answer_key(message: Message, key: str, markup=None, **extra):
    return await send_key(message.bot, message.chat.id, key, markup, message.from_user, **extra)


def _chat_id(event) -> int:
    if isinstance(event, CallbackQuery):
        return event.message.chat.id if event.message else event.from_user.id
    return event.chat.id


async def show_text(event, text: str, ents=None, markup=None):
    """Edit the message for callbacks (fallback: delete+send), send a new one for messages."""
    if isinstance(event, CallbackQuery):
        msg = event.message
        if isinstance(msg, Message):
            try:
                return await msg.edit_text(text, entities=ents or None, reply_markup=markup, parse_mode=None)
            except TelegramBadRequest as e:
                if "message is not modified" in str(e):
                    return msg
                try:
                    await msg.delete()
                except Exception:
                    pass
        return await send_text(event.bot, _chat_id(event), text, ents, markup)
    return await send_text(event.bot, event.chat.id, text, ents, markup)


async def show(event, key: str, markup=None, user=None, **extra):
    text, ents = T.render(key, user or event.from_user, **extra)
    return await show_text(event, text, ents, markup)


async def send_photo_caption(bot: Bot, chat_id: int, photo_id: str, text: str, ents=None, markup=None):
    cap = text[:1000]
    limit = u16len(cap)
    ents_ok = [e for e in (ents or []) if e.offset + e.length <= limit]
    try:
        return await bot.send_photo(chat_id, photo_id, caption=cap, caption_entities=ents_ok or None,
                                    reply_markup=markup, parse_mode=None)
    except TelegramBadRequest:
        try:
            return await bot.send_photo(chat_id, photo_id, caption=cap, reply_markup=markup, parse_mode=None)
        except TelegramBadRequest:
            return await send_text(bot, chat_id, text, ents, markup)


async def send_key_photo(bot: Bot, chat_id: int, photo_id: str | None, key: str, markup=None, user=None, **extra):
    text, ents = T.render(key, user, **extra)
    if photo_id:
        return await send_photo_caption(bot, chat_id, photo_id, text, ents, markup)
    return await send_text(bot, chat_id, text, ents, markup)


async def show_photo(event, photo_id: str, text: str, markup=None, ents=None):
    """Replace the current message with a photo+caption message."""
    if isinstance(event, CallbackQuery) and isinstance(event.message, Message):
        try:
            await event.message.delete()
        except Exception:
            pass
    return await send_photo_caption(event.bot, _chat_id(event), photo_id, text, ents, markup)
