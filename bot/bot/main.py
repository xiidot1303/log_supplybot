from bot.bot import *
from telegram import LoginUrl
from app.services.user_service import is_user_available_with_tg_id

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # check user is authenticated
    url = f"{WEBAPP_URL}"
    if await is_user_available_with_tg_id(update.effective_user.id):
        text = lang_dict['start text'][1]
        markup = await main_open_buttons()
    else:
        login_url = LoginUrl(url + "/telegram_login", request_write_access=True)
        text = lang_dict["you are not authenticated"][1]
        i_buttons = [[
            InlineKeyboardButton(text=lang_dict["authenticate"][1], login_url=login_url)
        ]]
        markup = InlineKeyboardMarkup(i_buttons)
    
    await update_message_reply_text(update, text, reply_markup=markup)