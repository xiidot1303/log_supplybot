from app.views import *
from app.services.statement_service import *

class StatementListView(LoginRequiredMixin, View):
    # @async_to_sync
    def get(self, request):
        context = {'statements': filter_uncompleted_statements()}
        return render(request, 'statement/statement_list.html', context)

class StatementCreateView(LoginRequiredMixin, CreateView):
    model = Statement
    form_class = StatementForm
    template_name = 'main/create.html'
    success_url = reverse_lazy('statement_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание документа'
        context['header'] = 'Документ'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user field
        return super().form_valid(form)

    
    