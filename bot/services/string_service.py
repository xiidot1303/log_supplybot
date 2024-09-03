from bot.services.language_service import *
from app.models import Statement, Request

async def statement_info_string(statement: Statement):
    text = ""
    for field in Statement._meta.get_fields():
        if field.name not in ["end", "request", 'user']:
            text += f"{field.verbose_name}: {getattr(statement, field.name)}\n"

    return text

async def statement_info_with_accepted_request_string(statement: Statement, request: Request):
    text = f"<b>{lang_dict['your request is accepted'][1]}</b>\n\n" \
        f"<i>{lang_dict['statement'][1]}:</i>\n"
    
    text += await statement_info_string(statement)

    text += f"\n<i>{lang_dict['your request'][1]}</i>:\n" \
        f"{Request._meta.get_field('price').verbose_name}: {request.price} {request.currency}\n" \
            f"{Request._meta.get_field('comment').verbose_name}: {request.comment}"
    
    return text

async def new_statement_info_to_managers_string(statement: Statement):
    text = f"🆕 <b>{lang_dict['new statement is created'][1]}</b>\n\n"
    text = text.format(
        user = statement.user
    )

    text += await statement_info_string(statement)

    text += f"\n{lang_dict['click button to make offer'][1]} 👇"
    return text
