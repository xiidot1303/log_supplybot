from app.views import *
from app.services.statement_service import *
from django.db import transaction

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

    
class StatementAndRequestCreateView(LoginRequiredMixin, View):
    def get(self, request):
        statement_form = StatementForm()
        request_form = RequestForm()
        context = {
            'forms': [statement_form, request_form],
            'title' :'Создание документа',
            'header': 'Документ'
        }
        return render(request, 'statement/statement_create.html', context)

    def post(self, request):
        statement_form = StatementForm(request.POST)
        request_form = RequestForm(request.POST)
        
        if statement_form.is_valid() and request_form.is_valid():
            with transaction.atomic():  # Ensure both forms are saved atomically
                # Save the Statement
                statement: Statement = statement_form.save(commit=False)
                statement.user = request.user
                country, city_name, *args = statement.pickup_address.split(',')
                city_name = city_name.strip()
                # get or create city by name
                city: City = get_or_create_city_by_name(city_name)
                statement.pickup = city
                statement.save()

                # Save the Request and link it to the Statement
                request_obj = request_form.save(commit=False)
                request_obj.user = request.user
                request_obj.statement = statement
                request_obj.save()

            return redirect('statement_list')  # Redirect to the statement list page after successful creation

        # If forms are not valid, render the page again with form errors
        context = {
            'forms': [statement_form, request_form],
            'title' :'Создание документа',
            'header': 'Документ'
        }
        return render(request, 'statement/statement_create.html', context)