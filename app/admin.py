from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import *

class Default(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class ManagerAdmin(UserAdmin):
    model = Manager

    fieldsets = UserAdmin.fieldsets + (
        ('Telegram', {'fields': ('tg_id',)}),
    )

admin.site.register(Statement, Default)
admin.site.register(Request, Default)
admin.site.register(Manager, ManagerAdmin)