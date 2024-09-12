from django.forms import ModelForm
from app.models import *
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField, SetPasswordForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class StatementForm(forms.ModelForm):
    class Meta:
        model = Statement
        fields = ['pickup', 'dropoff', 'shipment_date', 'end_date', 'transport_type', 'cargo', 'load_capacity', 'weight']  # Define the order of fields

        widgets = {
            'pickup': forms.Select(attrs={'class': 'form-control choicesjs'}),
            'dropoff': forms.Select(attrs={'class': 'form-control choicesjs'}),
            'shipment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'transport_type': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'load_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
            cleaned_data = super().clean()
            shipment_date = cleaned_data.get('shipment_date')
            end_date = cleaned_data.get('end_date')

            if end_date and shipment_date and end_date > shipment_date:
                self.add_error('end_date', 'Дата окончания не может быть позже даты отгрузки.')

            return cleaned_data

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['currency', 'price', 'comment']

        widgets = {
            'currency': forms.Select(attrs={'class': 'form-control'}), 
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'cols': 30})
        }

class ManagerCreateForm(UserCreationForm):
    class Meta:
        model = Manager
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'})
        }

class ManagerUpdateForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
    )

    class Meta:
        model = Manager
        fields = ['username', 'first_name', 'password', 'last_name']
        field_classes = {"username": UsernameField}

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'password': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }
    field_order = ['first_name', 'last_name', 'username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )

        user_id = kwargs['instance'].id  # Get the user's ID
        super().__init__(*args, **kwargs)
        # Dynamically set the password change URL in the help text
        url=reverse('manager_passwordchange', args=[user_id])
        help_text = _(
            "Пароли хранятся в зашифрованном виде, поэтому нет возможности посмотреть "
            "пароль этого пользователя, но вы можете изменить его используя "
            f'<a href="{url}">эту форму</a>.'
        ),
        self.fields['password'].help_text = help_text

class CustomSetPasswordForm(SetPasswordForm):
    # old_password = None  # Remove the old password field

    def save(self, commit=True):
        new_password = self.cleaned_data["new_password1"]
        if commit:
            self.user.set_password(new_password)
            self.user.save()
        return self.user