from app.services import *
from app.models import Statement, City

# @sync_to_async
def filter_uncompleted_statements():
    query = Statement.objects.filter(end = False)
    return query

def get_statement_by_id(id):
    obj = Statement.objects.get(id = id)
    return obj

def get_or_create_city_by_name(name):
    obj, is_created = City.objects.get_or_create(title = name)
    return obj