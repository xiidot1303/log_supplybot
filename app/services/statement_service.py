from app.services import *
from app.models import Statement

# @sync_to_async
def statements_all():
    query = Statement.objects.all()
    return query

def get_statement_by_id(id):
    obj = Statement.objects.get(id = id)
    return obj