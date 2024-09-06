from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    main, statement, request
)

urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("telegram_login", main.telegram_login),


    # statement
    path('', statement.StatementListView.as_view(), name='statement_list'),
    path('statement-list', statement.StatementListView.as_view(), name='statement_list'),
    path('statement-create', statement.StatementCreateView.as_view(), name='statement_create'),

    #request
    path('request-list/<int:statement_id>/', request.RequestListView.as_view(), name='request_list'),
    path('request-accept/<int:request_id>/<int:user_id>/', request.request_accept, name='request_accept'),

    # files
    re_path(r'^files/(?P<path>.*)$', main.get_file),


]
