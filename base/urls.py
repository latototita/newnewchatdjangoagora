from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby),
    path('room/', views.room),
    path('get_token/', views.getToken),
    path('dashboard',views.dashboard),
    path('create_member/', views.createMember),
    path('signin',views.signin,name='login'),
    path('logout',views.Logout,name='logout'),
    path('signup',views.signup,name='signup'),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]