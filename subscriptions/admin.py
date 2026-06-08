from django.contrib import admin
from .models import SubscriptionType, SubscriptionTypeService, Subscription


class SubscriptionTypeServiceInline(admin.TabularInline):
    model = SubscriptionTypeService
    extra = 1


@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'procedures_count', 'validity_days', 'discount_percent', 'total_price')
    inlines = [SubscriptionTypeServiceInline]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'subscription_type', 'purchase_date', 'procedures_left', 'payment_status')
    list_filter = ('payment_status',)
