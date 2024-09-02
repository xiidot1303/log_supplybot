from app.services import *
from app.models import Statement

# @sync_to_async
def filter_uncompleted_statements():
    query = Statement.objects.filter(end = False)
    return query

def get_statement_by_id(id):
    obj = Statement.objects.get(id = id)
    return obj