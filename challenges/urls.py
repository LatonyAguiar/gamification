from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('create/', views.create_challenge, name='create_challenge'),
    path('assign/', views.assign_challenge, name='assign_challenge'),
    path('list/', views.list_challenges, name='list_challenges'),
    path('details/<int:id>/', views.challenge_details, name='challenge_details'),
    path('accept/<int:broker_id>/', views.accept_challenge, name='accept_challenge'),
    
    # URLs para desafios
    path('edit_challenge/<int:id>/', views.edit_challenge, name='edit_challenge'),
    path('delete_challenge/<int:id>/', views.delete_challenge, name='delete_challenge'),
    
    # URLs para corretores
    path('create_broker/', views.create_broker, name='create_broker'),
    path('list_brokers/', views.list_brokers, name='list_brokers'),
    path('view_assigned_challenges/<int:broker_id>/', views.view_assigned_challenges, name='view_assigned_challenges'),
    path('accept_challenge/<int:broker_id>/', views.accept_challenge, name='accept_challenge'),
    path('edit_broker/<int:id>/', views.edit_broker, name='edit_broker'),
    path('delete_broker/<int:id>/', views.delete_broker, name='delete_broker'),
    
    # URLs para usuários
    path('create_user/', views.create_user, name='create_user'),
    path('list_users/', views.list_users, name='list_users'),
    path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('accept/<int:broker_id>/', views.accept_challenge, name='accept_challenge'),
]
