"""Default texts & settings. Everything here is editable from the admin panel after the first run."""

CATEGORIES = {
    "general": "🏠 عمومی",
    "buy": "💰 خرید اکانت",
    "gift": "🎁 گیفت",
    "ticket": "🎫 تیکت",
    "buttons": "🔘 دکمه‌ها",
}

# key: (category, title, default value, variables hint)
DEFAULT_TEXTS: dict[str, tuple[str, str, str, str]] = {
    # ---------------- general ----------------
    "welcome": ("general", "پیام خوشامدگویی",
        "👑 {first_name} عزیز، به LBank Buyer خوش آمدید\n{sep}\n"
        "✨ در این ربات می‌توانید درخواست خرید اکانت ثبت کنید، گیفت دریافت کنید و با تیم پشتیبانی در ارتباط باشید.\n{sep}\n"
        "🔽 یکی از گزینه‌های زیر را انتخاب کنید",
        "{first_name} {username} {user_id}"),
    "menu_title": ("general", "عنوان منوی اصلی",
        "🏠 منوی اصلی\n{sep}\nیکی از گزینه‌ها را انتخاب کنید:",
        "{first_name} {username} {user_id}"),
    "sub_required": ("general", "پیام عضویت اجباری",
        "🔒 دسترسی محدود\n{sep}\n📣 برای استفاده از ربات ابتدا در کانال‌های زیر عضو شوید و سپس دکمه «بررسی عضویت» را بزنید.",
        "{first_name} {username} {user_id}"),
    "sub_check_fail": ("general", "پیام عدم عضویت (هشدار)",
        "❌ هنوز در همه کانال‌ها عضو نشده‌اید.", ""),
    "blocked": ("general", "پیام مسدودی",
        "🚫 دسترسی شما به ربات مسدود شده است.", "{first_name}"),
    "rate_limited": ("general", "پیام جلوگیری از اسپم",
        "⏳ لطفاً کمی آهسته‌تر پیام ارسال کنید.", ""),
    "error_generic": ("general", "پیام خطای عمومی",
        "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کنید.", ""),
    "session_expired": ("general", "پیام منقضی‌شدن مرحله",
        "⌛️ این مرحله منقضی شده است. لطفاً از منوی اصلی دوباره شروع کنید.", ""),
    "rules": ("general", "قوانین",
        "📋 قوانین\n{sep}\n"
        "1️⃣ اطلاعات واردشده باید صحیح و دقیق باشد.\n"
        "2️⃣ هرگز رمز عبور، کد ورود، کد تأیید یا اطلاعات بازیابی ارسال نکنید.\n"
        "3️⃣ ثبت درخواست تکراری یا ساختگی منجر به مسدودی می‌شود.\n"
        "4️⃣ تصمیم نهایی درباره هر درخواست با مدیریت است.\n{sep}",
        ""),
    "support": ("general", "پیام پشتیبانی",
        "👨‍💻 پشتیبانی\n{sep}\n"
        "برای ارتباط مستقیم از دکمه زیر استفاده کنید، یا از بخش «ثبت تیکت» پیام خود را ثبت نمایید.",
        "{first_name}"),
    "profile": ("general", "حساب کاربری",
        "👤 حساب کاربری\n{sep}\n"
        "🆔 شناسه: {user_id}\n"
        "📛 نام: {first_name}\n"
        "🔗 یوزرنیم: {username}\n"
        "📅 عضویت: {joined}\n{sep}\n"
        "💰 درخواست‌ها: {requests_count}\n"
        "🎫 تیکت‌ها: {tickets_count}\n"
        "🎁 گیفت‌های دریافتی: {gifts_count}",
        "{first_name} {username} {user_id} {joined} {requests_count} {tickets_count} {gifts_count}"),
    "myreq_list": ("general", "لیست درخواست‌های کاربر",
        "📋 درخواست‌های شما\n{sep}\n{list}", "{list}"),
    "myreq_empty": ("general", "نبود درخواست",
        "📭 شما هنوز درخواستی ثبت نکرده‌اید.", ""),
    "request_status_update": ("general", "اعلان تغییر وضعیت درخواست",
        "📣 وضعیت درخواست شما تغییر کرد\n{sep}\n"
        "🆔 شماره درخواست: {request_id}\n💵 مبلغ: {amount} دلار\n📅 سال: {year}\n"
        "📊 وضعیت جدید: {status}\n📝 توضیحات: {note}",
        "{request_id} {amount} {year} {status} {note} {first_name}"),
    # ---------------- buy ----------------
    "buy_ask_amount": ("buy", "مرحله ۱ - پرسش مبلغ",
        "💰 مبلغ موردنظر خود را به دلار وارد کنید.\n\nمثال: 400 دلار", ""),
    "buy_amount_invalid": ("buy", "خطای مبلغ نامعتبر",
        "⚠️ مبلغ واردشده معتبر نیست. لطفاً فقط عدد وارد کنید.\n\nمثال: 400 دلار", ""),
    "buy_amount_confirm": ("buy", "تأیید مبلغ",
        "{sep}\n💵 مبلغ ثبت‌شده: {amount} دلار\n{sep}\n"
        "اگر درست است «تأیید» را بزنید؛ برای اصلاح، مبلغ جدید را بفرستید.",
        "{amount}"),
    "buy_ask_year": ("buy", "مرحله ۲ - پرسش سال",
        "📅 اکانت مربوط به چه سالی است؟\n\nمثال: 2026", ""),
    "buy_year_invalid": ("buy", "خطای سال نامعتبر",
        "⚠️ سال واردشده معتبر نیست. یک سال چهار رقمی وارد کنید.\n\nمثال: 2026", ""),
    "buy_year_confirm": ("buy", "تأیید سال",
        "{sep}\n📅 سال ثبت‌شده: {year}\n{sep}\n"
        "اگر درست است «تأیید» را بزنید؛ برای اصلاح، سال جدید را بفرستید.",
        "{year}"),
    "buy_ask_docs": ("buy", "مرحله ۳ - ارسال مدارک",
        "📎 لطفاً تصویر یا مدارک غیرحساس مربوط به درخواست خود را ارسال کنید.\n\n"
        "⚠️ هرگز رمز عبور، کد ورود، کد تأیید یا اطلاعات بازیابی ارسال نکنید.\n\n"
        "پس از ارسال، دکمه «اتمام ارسال مدارک» را بزنید.", ""),
    "buy_docs_received": ("buy", "تأیید دریافت مدرک",
        "✅ مدرک دریافت شد. (تعداد: {docs_count})\nمدرک دیگری دارید بفرستید، در غیر این صورت «اتمام ارسال مدارک» را بزنید.",
        "{docs_count}"),
    "buy_docs_invalid_text": ("buy", "خطای ارسال متن به‌جای مدرک",
        "⚠️ در این مرحله فقط تصویر یا فایل بفرستید.\n🔐 از ارسال رمز عبور و کدهای ورود/تأیید خودداری کنید.", ""),
    "buy_docs_limit": ("buy", "حداکثر تعداد مدارک",
        "⚠️ حداکثر ۱۰ مدرک قابل ارسال است. «اتمام ارسال مدارک» را بزنید.", ""),
    "buy_docs_required": ("buy", "اجباری بودن مدرک (هشدار)",
        "⚠️ لطفاً حداقل یک مدرک ارسال کنید.", ""),
    "buy_summary": ("buy", "مرحله ۴ - خلاصه نهایی",
        "📋 خلاصه درخواست\n{sep}\n💵 مبلغ: {amount} دلار\n📅 سال اکانت: {year}\n📎 تعداد مدارک: {docs_count}\n{sep}\n"
        "آیا ثبت نهایی را تأیید می‌کنید؟",
        "{amount} {year} {docs_count}"),
    "buy_success": ("buy", "مرحله ۵ - پیام موفقیت",
        "✅ درخواست شما با موفقیت ثبت شد.\n\n📨 درخواست شما برای مدیریت ارسال گردید.\n\n⏳ لطفاً منتظر بررسی باشید.\n\n🆔 شماره درخواست: {request_id}",
        "{request_id} {amount} {year}"),
    "buy_cancelled": ("buy", "پیام لغو",
        "❌ عملیات لغو شد.", ""),
    "buy_duplicate": ("buy", "درخواست تکراری",
        "⚠️ درخواستی با همین مبلغ و سال از شما در حال بررسی است. لطفاً منتظر نتیجه بمانید.", ""),
    "buy_limit": ("buy", "محدودیت درخواست باز",
        "⚠️ شما به سقف درخواست‌های در حال بررسی رسیده‌اید. لطفاً تا مشخص‌شدن نتیجه صبر کنید.", ""),
    # ---------------- gift ----------------
    "gift_list": ("gift", "لیست گیفت‌ها",
        "🎁 گیفت‌ها\n{sep}\nیکی از گیفت‌ها را انتخاب کنید:", ""),
    "gift_empty": ("gift", "نبود گیفت",
        "📭 در حال حاضر گیفتی موجود نیست.", ""),
    "gift_detail": ("gift", "جزئیات گیفت",
        "🎁 {gift_name}\n{sep}\n{gift_desc}\n{sep}\n📦 موجودی: {gift_stock}",
        "{gift_name} {gift_desc} {gift_stock}"),
    "gift_claimed": ("gift", "دریافت موفق گیفت",
        "🎉 تبریک! گیفت «{gift_name}» برای شما ثبت شد.", "{gift_name}"),
    "gift_out_of_stock": ("gift", "اتمام موجودی گیفت",
        "😔 موجودی این گیفت به پایان رسیده است.", "{gift_name}"),
    "gift_limit_reached": ("gift", "رسیدن به محدودیت دریافت",
        "⚠️ شما قبلاً سهمیه دریافت این گیفت را استفاده کرده‌اید.", "{gift_name}"),
    "gift_received_admin": ("gift", "گیفت ارسالی از طرف مدیریت",
        "🎁 مدیریت یک گیفت برای شما ارسال کرد!\n{sep}\n🎀 {gift_name}\n{gift_desc}",
        "{first_name} {gift_name} {gift_desc}"),
    # ---------------- ticket ----------------
    "ticket_menu": ("ticket", "منوی تیکت",
        "🎫 تیکت‌ها\n{sep}\nبرای ارتباط با پشتیبانی یک تیکت جدید ثبت کنید یا تیکت‌های قبلی را ببینید.", ""),
    "ticket_ask_title": ("ticket", "پرسش عنوان تیکت",
        "📝 عنوان تیکت را بنویسید:", ""),
    "ticket_title_invalid": ("ticket", "خطای عنوان",
        "⚠️ عنوان باید متنی بین ۳ تا 150 کاراکتر باشد.", ""),
    "ticket_ask_desc": ("ticket", "پرسش توضیحات تیکت",
        "🗒 توضیحات تیکت را بنویسید:", ""),
    "ticket_desc_invalid": ("ticket", "خطای توضیحات",
        "⚠️ توضیحات باید متنی حداکثر 3000 کاراکتر باشد.", ""),
    "ticket_ask_attach": ("ticket", "پرسش پیوست تیکت",
        "📎 در صورت نیاز تصویر یا فایل ارسال کنید، سپس «ثبت تیکت» را بزنید.\n⚠️ رمز عبور و کد ورود نفرستید.", ""),
    "ticket_attach_received": ("ticket", "دریافت پیوست",
        "✅ فایل دریافت شد. برای نهایی‌کردن «ثبت تیکت» را بزنید.", ""),
    "ticket_created": ("ticket", "تیکت ثبت شد",
        "✅ تیکت شما ثبت شد.\n🆔 شماره تیکت: {ticket_id}\n⏳ به‌زودی پاسخ داده می‌شود.", "{ticket_id} {title}"),
    "ticket_list": ("ticket", "عنوان لیست تیکت‌ها",
        "🎫 تیکت‌های شما\n{sep}\nبرای مشاهده یکی را انتخاب کنید:", ""),
    "ticket_list_empty": ("ticket", "نبود تیکت",
        "📭 شما هنوز تیکتی ثبت نکرده‌اید.", ""),
    "ticket_view": ("ticket", "نمایش تیکت",
        "🎫 تیکت #{ticket_id}\n📌 {title}\n📊 وضعیت: {status}\n{sep}\n{history}",
        "{ticket_id} {title} {status} {history}"),
    "ticket_ask_reply": ("ticket", "پرسش پاسخ کاربر",
        "✍️ پیام خود را بنویسید (متن، تصویر یا فایل):", ""),
    "ticket_reply_sent": ("ticket", "ارسال پاسخ کاربر",
        "✅ پیام شما ثبت شد و برای پشتیبانی ارسال گردید.", "{ticket_id}"),
    "ticket_admin_replied": ("ticket", "اعلان پاسخ ادمین",
        "📩 پاسخ جدید برای تیکت #{ticket_id}\n📌 {title}\n{sep}\n{reply}",
        "{ticket_id} {title} {reply}"),
    "ticket_closed": ("ticket", "پیام بسته‌شدن تیکت",
        "🔒 تیکت #{ticket_id} بسته شد.", "{ticket_id} {title}"),
    "ticket_already_closed": ("ticket", "تیکت بسته است",
        "🔒 این تیکت بسته شده و امکان ارسال پیام جدید ندارد.", ""),
    "ticket_not_found": ("ticket", "تیکت پیدا نشد",
        "⚠️ تیکت پیدا نشد.", ""),
    # ---------------- buttons ----------------
    "btn_buy": ("buttons", "دکمه خرید اکانت", "💰 خرید اکانت", ""),
    "btn_gift": ("buttons", "دکمه گیفت", "🎁 گیفت", ""),
    "btn_ticket": ("buttons", "دکمه ثبت تیکت", "🎫 ثبت تیکت", ""),
    "btn_support": ("buttons", "دکمه پشتیبانی", "👨‍💻 پشتیبانی", ""),
    "btn_rules": ("buttons", "دکمه قوانین", "📋 قوانین", ""),
    "btn_profile": ("buttons", "دکمه حساب کاربری", "👤 حساب کاربری", ""),
    "btn_admin_panel": ("buttons", "دکمه پنل مدیریت", "👑 پنل مدیریت", ""),
    "btn_confirm": ("buttons", "دکمه تأیید", "✅ تأیید", ""),
    "btn_cancel": ("buttons", "دکمه لغو", "❌ لغو", ""),
    "btn_back": ("buttons", "دکمه بازگشت", "🔙 بازگشت", ""),
    "btn_home": ("buttons", "دکمه منوی اصلی", "🏠 منوی اصلی", ""),
    "btn_check_sub": ("buttons", "دکمه بررسی عضویت", "✅ بررسی عضویت", ""),
    "btn_finish_docs": ("buttons", "دکمه اتمام مدارک", "📨 اتمام ارسال مدارک", ""),
    "btn_claim_gift": ("buttons", "دکمه دریافت گیفت", "🎁 دریافت گیفت", ""),
    "btn_new_ticket": ("buttons", "دکمه تیکت جدید", "➕ تیکت جدید", ""),
    "btn_my_tickets": ("buttons", "دکمه تیکت‌های من", "📂 تیکت‌های من", ""),
    "btn_reply": ("buttons", "دکمه پاسخ", "💬 ارسال پیام", ""),
    "btn_close_ticket": ("buttons", "دکمه بستن تیکت", "🔒 بستن تیکت", ""),
    "btn_finish_ticket": ("buttons", "دکمه ثبت نهایی تیکت", "✅ ثبت تیکت", ""),
    "btn_my_requests": ("buttons", "دکمه درخواست‌های من", "📋 درخواست‌های من", ""),
    "btn_contact_support": ("buttons", "دکمه ارتباط با پشتیبان", "💬 ارتباط با پشتیبان", ""),
    "btn_view_ticket": ("buttons", "دکمه مشاهده تیکت", "👁 مشاهده تیکت", ""),
}

DEFAULT_SETTINGS: dict[str, str] = {
    "separator": "━━━━━━━━━━━━━━━",
    "support_username": "",
    "docs_required": "1",
    "premium_emoji": "1",
    "max_open_requests": "5",
    "min_amount": "1",
    "max_amount": "1000000",
    "rate_limit_events": "15",
    "rate_limit_window": "10",
    "backup_enabled": "1",
    "backup_interval_hours": "24",
    "custom_emojis": "{}",
}

# key: (title, type)   type: text | int | bool
SETTINGS_META: dict[str, tuple[str, str]] = {
    "support_username": ("یوزرنیم پشتیبان", "text"),
    "docs_required": ("اجباری‌بودن مدرک خرید", "bool"),
    "premium_emoji": ("ایموجی پرمیوم", "bool"),
    "max_open_requests": ("سقف درخواست باز هر کاربر", "int"),
    "min_amount": ("حداقل مبلغ (دلار)", "int"),
    "max_amount": ("حداکثر مبلغ (دلار)", "int"),
    "rate_limit_events": ("ضداسپم: تعداد پیام مجاز", "int"),
    "rate_limit_window": ("ضداسپم: بازه (ثانیه)", "int"),
    "backup_enabled": ("پشتیبان‌گیری خودکار", "bool"),
    "backup_interval_hours": ("فاصله پشتیبان‌گیری (ساعت)", "int"),
}

SAMPLE_VARS = {
    "first_name": "علی", "username": "@example", "user_id": "123456789",
    "amount": "400", "year": "2026", "request_id": "101", "status": "✅ تأیید شده",
    "note": "—", "docs_count": "2", "list": "#1 • 400$ • 2026", "joined": "2026-01-01",
    "requests_count": "3", "tickets_count": "1", "gifts_count": "2",
    "gift_name": "گیفت ویژه", "gift_desc": "توضیحات گیفت", "gift_stock": "10",
    "ticket_id": "55", "title": "عنوان نمونه", "reply": "متن پاسخ نمونه", "history": "— تاریخچه —",
}
