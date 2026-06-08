from django.contrib import admin
from .models import Service, PortfolioPhoto


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price')
    search_fields = ('name',)


@admin.register(PortfolioPhoto)
class PortfolioPhotoAdmin(admin.ModelAdmin):
    list_display = ('master', 'description', 'uploaded_at')
