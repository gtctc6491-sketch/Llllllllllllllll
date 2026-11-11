from bot.keyboards.common import btn, ikb, tb


def main_menu(is_admin: bool = False):
    rows = [
        [btn(tb("btn_buy"), "buy")],
        [btn(tb("btn_gift"), "gift"), btn(tb("btn_ticket"), "ticket")],
        [btn(tb("btn_support"), "support"), btn(tb("btn_rules"), "rules")],
        [btn(tb("btn_profile"), "profile")],
    ]
    if is_admin:
        rows.append([btn(tb("btn_admin_panel"), "a:home")])
    return ikb(rows)


def home_row():
    return [btn(tb("btn_home"), "menu")]


def home_only():
    return ikb([home_row()])


def confirm_cancel(ok: str = "buy_ok", cancel: str = "buy_cancel"):
    return ikb([[btn(tb("btn_confirm"), ok), btn(tb("btn_cancel"), cancel)]])


def cancel_only(cancel: str = "buy_cancel"):
    return ikb([[btn(tb("btn_cancel"), cancel)]])


def docs_kb():
    return ikb([[btn(tb("btn_finish_docs"), "buy_docs_done")], [btn(tb("btn_cancel"), "buy_cancel")]])
