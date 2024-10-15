from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/app/', include('app.urls')),
    path('auth/', include('djoser.urls')),
    path('api/v1/users/', include('users.urls')),
]
