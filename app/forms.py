from django.forms import ModelForm
from app.models import *
from django import forms

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

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['currency', 'price', 'comment']

        widgets = {
            'currency': forms.Select(attrs={'class': 'form-control'}), 
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'cols': 30})
        }