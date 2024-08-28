from bot.bot import *
from bot.services.string_service import *

async def request_accepted_notify_job(context: CustomContext):
    user_id, statement, request = context.job.data
    text = await statement_info_with_accepted_request_string(statement, request)
    await send_newsletter(bot, user_id, text, pin_message=True)