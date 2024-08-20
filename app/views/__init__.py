from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from app.forms import *
from django.urls import reverse_lazy
from typing import Dict, Any
from django.contrib import messages
from app.utils.deco import *
from django.utils.decorators import method_decorator
from django.views import View
from django import http

async def redirect_back(request):
    return redirect(request.META.get('HTTP_REFERER'))