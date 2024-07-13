from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('challenges/', include('challenges.urls')),
    path('', views.login_view, name='login'),
    path('home/', views.HomeView.as_view(), name='home'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), # Pode solicitar todos os arquivos MEDIA_ROOT em settings.py
]
