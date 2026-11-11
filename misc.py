from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.common import btn, ikb, pager_row, tb
from bot.keyboards.user import home_row
from bot.services.messaging import show
from bot.services.settings import cfg
from database.models import Request, Ticket, User, UserGift
from utils.helpers import (PAGE_SIZE, REQUEST_EMOJI, REQUEST_STATUS, clamp_page, fmt_amount, fmt_dt,
                           page_count)

router = Router()


@router.callback_query(F.data == "rules")
async def rules(cb: CallbackQuery):
    await cb.answer()
    await show(cb, "rules", ikb([home_row()]))


@router.callback_query(F.data == "support")
async def support(cb: CallbackQuery):
    await cb.answer()
    uname = cfg.get("support_username").lstrip("@").strip()
    rows = []
    if uname:
        rows.append([btn(tb("btn_contact_support"), url=f"https://t.me/{uname}")])
    rows.append([btn(tb("btn_ticket"), "ticket")])
    rows.append(home_row())
    await show(cb, "support", ikb(rows))


@router.callback_query(F.data == "profile")
async def profile(cb: CallbackQuery, session: AsyncSession, db_user: User):
    await cb.answer()
    uid = cb.from_user.id
    rc = await session.scalar(select(func.count(Request.id)).where(Request.user_id == uid))
    tc = await session.scalar(select(func.count(Ticket.id)).where(Ticket.user_id == uid))
    gc = await session.scalar(select(func.count(UserGift.id)).where(UserGift.user_id == uid))
    kb = ikb([[btn(tb("btn_my_requests"), "myreq:0")], home_row()])
    await show(cb, "profile", kb, joined=fmt_dt(db_user.joined_at),
               requests_count=rc or 0, tickets_count=tc or 0, gifts_count=gc or 0)


@router.callback_query(F.data.startswith("myreq:"))
async def my_requests(cb: CallbackQuery, session: AsyncSession):
    await cb.answer()
    uid = cb.from_user.id
    page = int(cb.data.split(":")[1])
    total = await session.scalar(select(func.count(Request.id)).where(Request.user_id == uid)) or 0
    if total == 0:
        await show(cb, "myreq_empty", ikb([home_row()]))
        return
    pages = page_count(total)
    page = clamp_page(page, pages)
    q = (select(Request).where(Request.user_id == uid).order_by(Request.id.desc())
         .offset(page * PAGE_SIZE).limit(PAGE_SIZE))
    rows = (await session.execute(q)).scalars().all()
    lines = [
        f"{REQUEST_EMOJI.get(r.status, '•')} #{r.id} • {fmt_amount(r.amount)}$ • {r.year}\n"
        f"   {REQUEST_STATUS.get(r.status, r.status)} • {fmt_dt(r.created_at)}"
        for r in rows
    ]
    kb = ikb([pager_row(lambda p: f"myreq:{p}", page, pages), home_row()])
    await show(cb, "myreq_list", kb, list="\n".join(lines))
