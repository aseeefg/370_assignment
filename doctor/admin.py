from django.contrib import admin
from .models import Doctor
from .models import Appointment


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('specialization','available_days','available_time')
    filter_horizontal=()
    list_filter=()
    fieldsets = ()
# Register your models here.
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Appointment)

