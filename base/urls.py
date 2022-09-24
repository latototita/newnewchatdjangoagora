from django.urls import path
from . import views
app_name='base'

urlpatterns = [
    path('', views.index, name='index'),
    path('lobby', views.lobby, name='lobby'),
    path('pusher/auth/', views.pusher_auth, name='agora-pusher-auth'),
    path('token/', views.generate_agora_token, name='agora-token'),
    path('call-user/', views.call_user, name='agora-call-user'),
    path('room/', views.room,name='room'),
    path('get_token/', views.getToken),
    path('dashboard',views.dashboard,name='dashboard'),
    path('create_member/', views.createMember),
    path('signin',views.signin,name='login'),
    path('logout',views.Logout,name='logout'),
    path('signup',views.signup,name='signup'),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
    path('terms', views.terms,name='terms'),
]