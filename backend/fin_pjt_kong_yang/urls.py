"""
URL configuration for fin_pjt_kong_yang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import CustomUserDetailsView
from dj_rest_auth.views import UserDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 회원가입 관련 url
    path('users/',include('users.urls')),
    path('products/',include('fin_products.urls')),
    # path('users/signup/', include('dj_rest_auth.registration.urls'))
    
    # 회원정보 관련 url
    path('users/user/', CustomUserDetailsView.as_view()),  # ✅ 덮어쓰기
    path('users/', include('dj_rest_auth.urls')),
    path('accounts/user/', UserDetailsView.as_view(), name='rest_user_details'),
    # 글
    path('api/v1/', include('articles.urls')),
    #지수비교
    path('api/', include('commodities.urls')),
]
