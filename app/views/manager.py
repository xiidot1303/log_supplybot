from app.views import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm


@login_required
@group_required('controller')
def manager_list(request):
    managers = filter_managers()
    context = {
        "managers": managers
    }
    return render(request, 'manager/manager_list.html', context)

class ManagerCreateView(LoginRequiredMixin, PermissionDenied, CreateView):
    permission_required = 'app.add_manager'
    model = User
    form_class = ManagerCreateForm
    template_name = 'manager/manager_update.html'
    success_url = reverse_lazy('manager_list')


class ManagerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'app.change_manager'
    model = User
    form_class = ManagerUpdateForm
    template_name = 'manager/manager_update.html'
    success_url = reverse_lazy('manager_list')

class ManagerPasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'app.change_manager'
    template_name = 'manager/manager_password_change.html'
    
    def get(self, request, pk):
        user = Manager.objects.get(pk=pk)
        form = SetPasswordForm(user=user)
        return render(request, self.template_name, {'form': form, 'manager': user})

    def post(self, request, pk):
        manager = Manager.objects.get(pk=pk)
        form = SetPasswordForm(user=manager, data=request.POST)
        if form.is_valid():
            form.save()
            # update_session_auth_hash(request, form.user)  # Keep user logged in after password change
            return redirect(reverse_lazy('manager_list'))  # Redirect to a page after successful password change
        return render(request, self.template_name, {'form': form, 'manager': manager})

@login_required
@permission_required('app.delete_manager')
def manager_delete(request, pk):
    manager = get_user_by_pk(pk)
    manager.delete()
    return redirect_back(request)