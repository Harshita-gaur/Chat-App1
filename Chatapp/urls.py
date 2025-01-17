from django.urls import path
from . import views

urlpatterns = [
    path('send_message/<str:receiver_id>/', views.send_message, name='send_message'),  
    path('logout/', views.logout_view, name='logout'),
    path('send_group_message/<str:sender_id>/', views.send_group_message, name='send_group_message'),
    path('chat/', views.chat, name='chat'),
    path('chat/group/<str:sender_id>/', views.chat_with_group, name='chat_with_group'),
    path('chat/user/<str:receiver_id>/', views.chat_with_user, name='chat_with_user'),
    path('login/', views.login_user, name='login_user'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
]
