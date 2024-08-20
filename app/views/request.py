from app.views import *
from app.services.request_service import *
from app.services.statement_service import *

class RequestListView(LoginRequiredMixin, View):
    template_name = 'request/request_list.html'

    def setup(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        statement_id = kwargs['statement_id']
        # setup request objects
        self.requests_of_others = filter_requests_by_statement(statement_id, request.user.id)
        self.request_of_user = get_request_of_user_by_statement(statement_id, request.user.id)
        # set form
        self.form = RequestForm(request.POST or None, instance=self.request_of_user)
        # set context
        self.context = {
            "requests_of_others": self.requests_of_others,
            "request_of_user": self.request_of_user,
            "form": self.form
        }

    def get(self, request, **kwargs):
        context = self.context
        return render(request, self.template_name, context)

    def post(self, request, statement_id):
        form = self.form
        context = self.context
        if form.is_valid():
            form.instance.user = request.user
            form.instance.statement = get_statement_by_id(statement_id)
            form.save()
            return redirect('request_list', statement_id=statement_id)
    
        return render(request, self.template_name, context) 



# class RequestCreateView(LoginRequiredMixin, CreateView):
#     model = Request
#     form_class = RequestForm
#     template_name = 'main/create.html'
#     success_url = reverse_lazy('request_list', kwargs = {'statement_pk': })