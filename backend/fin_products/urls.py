from django.urls import path
from . import views

app_name="products"
urlpatterns = [
    path('deposits/', views.deposit_products_view, name='deposits'),
    path('savings/', views.savings_products_view, name='savings'),
    # path('recommend/', views.recommend_products, name='recommend'),
     path('deposit/<int:pk>/', views.DepositProductDetailView.as_view(), name='deposit-detail'),
    path('savings/<int:pk>/', views.SavingsProductDetailView.as_view(), name='savings-detail'),
    path('recommend/', views.recommend_products, name='recommend-products'),
    
]
