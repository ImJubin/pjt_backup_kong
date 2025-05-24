from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list_create),
    # path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/create/', views.create_aritcle),
    path('articles/<int:article_pk>/comments/', views.comment_create),
    # path('articles/<int:article_id>/comments/', views.comment_list_create),
    # path('comments/<int:comment_id>/like/', views.comment_like),    
]