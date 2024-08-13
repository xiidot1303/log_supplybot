from app.services import *
from app.models import Request

def filter_requests_by_statement(statement_id, user_id):
    query = Request.objects.filter(statement__id = statement_id).exclude(user__id = user_id)
    return query

def get_request_of_user_by_statement(statement_id, user_id):
    query = Request.objects.filter(statement__id = statement_id, user__id = user_id)
    return query.first() if query.exists() else None