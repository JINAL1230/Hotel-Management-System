from django.urls import path
from . import views

urlpatterns = [
    path('adminlogin/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='logout'),
    path('', views.dashboard_home, name='dashboard_home'),
    path('rooms/', views.rooms_detail, name='rooms_detail'),
    path('customers/', views.customers_detail, name='customers_detail'),
    path('bookings/', views.bookings_detail, name='bookings_detail'),
    path('payments/',views.payment_dashboard,name='payment_dashboard'),
]
