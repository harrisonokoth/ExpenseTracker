from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('chart/', views.chart_view, name='chart_view'),
    path('login/', views.login_view, name='login'),  # Ensure this line is present
    path('logout/', views.logout_view, name='logout'),
]
