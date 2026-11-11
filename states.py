from aiogram.fsm.state import State, StatesGroup


class BuyStates(StatesGroup):
    amount = State()
    amount_confirm = State()
    year = State()
    year_confirm = State()
    docs = State()
    final = State()


class TicketStates(StatesGroup):
    title = State()
    description = State()
    attach = State()
    reply = State()


class AdminStates(StatesGroup):
    search_user = State()
    user_message = State()
    search_request = State()
    request_note = State()
    request_message = State()
    gift_name = State()
    gift_photo = State()
    gift_desc = State()
    gift_stock = State()
    gift_limit = State()
    gift_edit = State()
    gift_send_user = State()
    real_gift_user = State()
    ticket_reply = State()
    broadcast_content = State()
    text_edit = State()
    emoji_add_emoji = State()
    emoji_add_name = State()
    separator_edit = State()
    channel_add = State()
    channel_link = State()
    admin_add_id = State()
    setting_edit = State()
