import json

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.common import btn, ikb
from bot.keyboards.user import cancel_only, confirm_cancel, docs_kb, main_menu
from bot.services.messaging import answer_key, show, send_key
from bot.services.notify import notify_admins, admins_with, send_file
from bot.services.settings import cfg
from bot.services.texts import T
from bot.states import BuyStates
from database.models import Request, User, utcnow
from utils.helpers import fmt_amount, parse_amount, parse_year, uname

router = Router()
ACTIVE = ("pending", "in_review")


@router.callback_query(F.data == "buy")
async def buy_start(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.clear()
    await state.set_state(BuyStates.amount)
    await show(cb, "buy_ask_amount", cancel_only())


@router.callback_query(F.data == "buy_cancel")
async def buy_cancel(cb: CallbackQuery, state: FSMContext, is_admin: bool):
    await cb.answer()
    await state.clear()
    await show(cb, "buy_cancelled", main_menu(is_admin))


# ---------------- step 1: amount ----------------
@router.message(StateFilter(BuyStates.amount, BuyStates.amount_confirm), F.text)
async def got_amount(message: Message, state: FSMContext):
    amount = parse_amount(message.text)
    if amount is None or not (cfg.int("min_amount") <= amount <= cfg.int("max_amount")):
        await answer_key(message, "buy_amount_invalid", cancel_only())
        return
    await state.update_data(amount=amount)
    await state.set_state(BuyStates.amount_confirm)
    await answer_key(message, "buy_amount_confirm", confirm_cancel(), amount=fmt_amount(amount))


@router.message(StateFilter(BuyStates.amount, BuyStates.amount_confirm))
async def amount_not_text(message: Message):
    await answer_key(message, "buy_amount_invalid", cancel_only())


@router.callback_query(F.data == "buy_ok", BuyStates.amount_confirm)
async def amount_ok(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(BuyStates.year)
    await show(cb, "buy_ask_year", cancel_only())


# ---------------- step 2: year ----------------
@router.message(StateFilter(BuyStates.year, BuyStates.year_confirm), F.text)
async def got_year(message: Message, state: FSMContext):
    year = parse_year(message.text)
    if year is None:
        await answer_key(message, "buy_year_invalid", cancel_only())
        return
    await state.update_data(year=year)
    await state.set_state(BuyStates.year_confirm)
    await answer_key(message, "buy_year_confirm", confirm_cancel(), year=year)


@router.message(StateFilter(BuyStates.year, BuyStates.year_confirm))
async def year_not_text(message: Message):
    await answer_key(message, "buy_year_invalid", cancel_only())


@router.callback_query(F.data == "buy_ok", BuyStates.year_confirm)
async def year_ok(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(docs=[])
    await state.set_state(BuyStates.docs)
    await show(cb, "buy_ask_docs", docs_kb())


# ---------------- step 3: documents ----------------
@router.message(BuyStates.docs, F.photo | F.document)
async def got_doc(message: Message, state: FSMContext):
    data = await state.get_data()
    docs = data.get("docs", [])
    if len(docs) >= 10:
        await answer_key(message, "buy_docs_limit", docs_kb())
        return
    if message.photo:
        docs.append({"t": "photo", "f": message.photo[-1].file_id})
    else:
        docs.append({"t": "document", "f": message.document.file_id, "n": message.document.file_name or ""})
    await state.update_data(docs=docs)
    await answer_key(message, "buy_docs_received", docs_kb(), docs_count=len(docs))


@router.message(BuyStates.docs)
async def docs_wrong(message: Message):
    # never accept free text here: protects users from pasting passwords / codes
    await answer_key(message, "buy_docs_invalid_text", docs_kb())


@router.callback_query(F.data == "buy_docs_done", BuyStates.docs)
async def docs_done(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    docs = data.get("docs", [])
    if cfg.bool("docs_required") and not docs:
        await cb.answer(T.plain("buy_docs_required", cb.from_user), show_alert=True)
        return
    await cb.answer()
    await state.set_state(BuyStates.final)
    await show(cb, "buy_summary", confirm_cancel(), amount=fmt_amount(data["amount"]),
               year=data["year"], docs_count=len(docs))


# ---------------- step 4/5: final confirm & save ----------------
@router.callback_query(F.data == "buy_ok", BuyStates.final)
async def submit(cb: CallbackQuery, state: FSMContext, session: AsyncSession, bot, db_user: User, is_admin: bool):
    await cb.answer()
    data = await state.get_data()
    await state.clear()
    uid = cb.from_user.id
    amount, year, docs = data.get("amount"), data.get("year"), data.get("docs", [])
    if amount is None or year is None:
        await show(cb, "session_expired", main_menu(is_admin))
        return

    dup = await session.scalar(select(func.count(Request.id)).where(
        Request.user_id == uid, Request.amount == amount, Request.year == year, Request.status.in_(ACTIVE)))
    if dup:
        await show(cb, "buy_duplicate", main_menu(is_admin))
        return
    open_count = await session.scalar(select(func.count(Request.id)).where(
        Request.user_id == uid, Request.status.in_(ACTIVE))) or 0
    if open_count >= cfg.int("max_open_requests"):
        await show(cb, "buy_limit", main_menu(is_admin))
        return

    req = Request(user_id=uid, amount=amount, year=year, docs=json.dumps(docs), status="pending",
                  created_at=utcnow(), updated_at=utcnow())
    session.add(req)
    await session.flush()
    await show(cb, "buy_success", main_menu(is_admin), request_id=req.id, amount=fmt_amount(amount), year=year)

    sep = cfg.get("separator")
    text = (f"🔔 درخواست جدید #{req.id}\n{sep}\n"
            f"👤 {db_user.first_name} • {uname(db_user.username)} • {uid}\n"
            f"💵 مبلغ: {fmt_amount(amount)} دلار\n📅 سال اکانت: {year}\n📎 مدارک: {len(docs)} فایل")
    kb = ikb([[btn("🔎 مشاهده و بررسی", f"a:r:{req.id}")]])
    await notify_admins(bot, session, "requests", text, kb)
    for admin in await admins_with(session, "requests"):
        for d in docs:
            try:
                await send_file(bot, admin.user_id, d["t"], d["f"], caption=f"📎 مدرک درخواست #{req.id}")
            except Exception:
                pass


@router.callback_query(F.data.in_({"buy_ok", "buy_docs_done"}))
async def stale(cb: CallbackQuery, is_admin: bool):
    await cb.answer()
    await show(cb, "session_expired", main_menu(is_admin))
