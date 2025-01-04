from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('customer/<str:username>/', views.customer_page, name='customer_page'),
    path('admin/<str:username>/', views.admin_page, name='admin_page'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('delete_customer/', views.delete_customer, name='delete_customer'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_customer_password/', views.change_customer_password, name='change_customer_password'),
    path('create_admin/', views.create_admin, name='create_admin'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('logout/', views.logout_view, name='logout'),
]