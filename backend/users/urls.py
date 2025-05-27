from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('account/', views.user_accounts, name='user-accounts'),
    path('calendar/', views.calendar_dates),
    path('purchase/', views.purchase_product, name='purchase_product'),
    path('update-interest/', views.update_interest),  # ✅ 이자 갱신용 API
    path('my-interest/', views.my_interest_comparison),
]
