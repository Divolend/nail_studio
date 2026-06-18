"""
Корневая маршрутизация проекта «Студия маникюра».
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),          # главная, услуги, мастера
    path('accounts/', include('accounts.urls')), # регистрация, вход, кабинеты
    path('booking/', include('booking.urls')),   # запись на процедуры
    path('subscriptions/', include('subscriptions.urls')),  # абонементы
    path('manage/', include('management.urls')),  # панель управления (админ)
]

# Раздача загруженных медиафайлов (работает и при DEBUG=False на хостинге).
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
