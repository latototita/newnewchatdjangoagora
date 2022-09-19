from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('base.urls',namespace='base')),
    path('', include('agora.urls',namespace='agora')),
]
