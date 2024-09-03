from bot.bot import *
from bot.services.string_service import *
from app.models import Statement, Manager
from config import WEBHOOK_URL, WEBAPP_URL

async def request_accepted_notify_job(context: CustomContext):
    user_id, statement, request = context.job.data
    text = await statement_info_with_accepted_request_string(statement, request)
    await send_newsletter(bot, user_id, text, pin_message=True)
    
async def new_statement_info_to_managers_notify_job(context: CustomContext):
    statement: Statement = context.job.data
    text = await new_statement_info_to_managers_string(statement)
    async for manager in Manager.objects.filter().exclude(id = statement.user.id):
        manager: Manager
        url = f"{WEBAPP_URL}/request-list/{statement.id}/"
        webapp = WebAppInfo(url)
        i_buttons = [
            [InlineKeyboardButton(text=f"📱 {lang_dict['make offer'][1]}", web_app=webapp)],
            [InlineKeyboardButton(text=f"🌐 {lang_dict['make offer'][1]}", url=url)]
        ]
        markup = InlineKeyboardMarkup(i_buttons)
        await send_newsletter(bot, manager.tg_id, text, reply_markup=markup)
