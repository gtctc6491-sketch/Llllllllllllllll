from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.user import main_menu
from bot.services.messaging import answer_key, show
from bot.services.subscription import forget, get_missing, send_sub_required
from bot.services.texts import T

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession, bot, is_admin: bool):
    await state.clear()
    missing = await get_missing(bot, session, message.from_user.id)
    if missing:
        await send_sub_required(message, missing)
        return
    await answer_key(message, "welcome", main_menu(is_admin))


@router.callback_query(F.data == "check_sub")
async def check_sub(cb: CallbackQuery, state: FSMContext, session: AsyncSession, bot, is_admin: bool):
    forget(cb.from_user.id)
    missing = await get_missing(bot, session, cb.from_user.id)
    if missing:
        await cb.answer(T.plain("sub_check_fail", cb.from_user), show_alert=True)
        await send_sub_required(cb, missing)
        return
    await cb.answer()
    await state.clear()
    await show(cb, "welcome", main_menu(is_admin))


@router.callback_query(F.data == "menu")
async def menu(cb: CallbackQuery, state: FSMContext, is_admin: bool):
    await state.clear()
    await cb.answer()
    await show(cb, "menu_title", main_menu(is_admin))


@router.callback_query(F.data == "noop")
async def noop(cb: CallbackQuery):
    await cb.answer()
