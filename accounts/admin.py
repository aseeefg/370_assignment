from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('user_id','email', 'first_name', 'last_name', 'phone_number', 'is_admin', 'is_patient' , 'is_doctor','date_joined')
    filter_horizontal=()
    list_filter=()
    fieldsets = ()
admin.site.register(Account,AccountAdmin)