from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('thankyou/', views.thank_you, name='thank_you'),
]