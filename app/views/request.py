from app.views import *
from app.services.request_service import *

class RequestListView(LoginRequiredMixin, View):
    def get(self, request, statement_id):
        requests_of_others = filter_requests_by_statement(statement_id, request.user.id)
        request_of_user = get_request_of_user_by_statement(statement_id, request.user.id)
        context = {
            "requests_of_others": requests_of_others,
            "request_of_user": request_of_user
        }
        return render(request, 'request/request_list.html', context)

# class RequestCreateView(LoginRequiredMixin, CreateView):
#     model = Request
#     form_class = RequestForm
#     template_name = 'main/create.html'
#     success_url = reverse_lazy('request_list', kwargs = {'statement_pk': })