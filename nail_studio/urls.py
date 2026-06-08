"""
Корневая маршрутизация проекта «Студия маникюра».
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),          # главная, услуги, мастера
    path('accounts/', include('accounts.urls')), # регистрация, вход, кабинеты
    path('booking/', include('booking.urls')),   # запись на процедуры
    path('subscriptions/', include('subscriptions.urls')),  # абонементы
    path('manage/', include('management.urls')),  # панель управления (админ)
]

# Раздача медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
