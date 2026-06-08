from django.contrib import admin
from .models import TimeSlot, Appointment


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('master', 'date', 'start_time', 'duration_minutes', 'status')
    list_filter = ('status', 'date')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'time_slot', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
