from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('chat/<str:receiver_id>/', views.chat_with_user, name='chat_with_user'), 
    path('send_message/<str:receiver_id>/', views.send_message, name='send_message'),  
    path('logout/', views.logout_view, name='logout'),
]
