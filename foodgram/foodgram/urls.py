from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken import views

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
