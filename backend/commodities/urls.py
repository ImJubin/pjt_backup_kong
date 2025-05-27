# commodities/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('commodity-history/', views.commodity_history, name='commodity_history'),
]