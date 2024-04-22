from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send/', views.send_email, name='send'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/<str:token>/', views.confirm_subscription, name='confirm_subscription'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('unsubscribe/<str:token>/', views.confirm_unsubscription, name='confirm_unsubscription'),
    path('members/', views.mailing_list_members, name='members'),
    path('mails/', views.email_list, name='mails'),
    path('mails/<int:mail_id>/', views.email_detail, name='email_detail'),
    path('mails/<int:mail_id>/delete/', views.delete_email, name='delete_email'),
]
