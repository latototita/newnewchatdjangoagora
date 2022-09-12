from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('base.urls')),
    path('', include('agora.urls',namespace='agora')),
]
