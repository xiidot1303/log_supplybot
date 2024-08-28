from bot.services.language_service import *
from app.models import Statement, Request

async def statement_info_with_accepted_request_string(statement: Statement, request: Request):
    text = f"<b>{lang_dict['your request is accepted'][1]}</b>\n\n" \
        f"<i>{lang_dict['statement'][1]}:</i>\n"
    
    for field in Statement._meta.get_fields():
        if field.name not in ["end", "request"]:
            text += f"{field.verbose_name}: {getattr(statement, field.name)}\n"

    text += f"\n<i>{lang_dict['your request'][1]}</i>:\n" \
        f"{Request._meta.get_field('price').verbose_name}: {request.price} {request.currency}\n" \
            f"{Request._meta.get_field('comment').verbose_name}: {request.comment}"
    
    return text
