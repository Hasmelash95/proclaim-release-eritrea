from django.urls import path
from . import views

# Url patterns for the press app

urlpatterns = [
    path('', views.PressList.as_view(), name='home'),
    path('article-filter/', views.article_filter, name='filter'),
    path('favorites/', views.favorites, name='favorites'),
    path('post-article/', views.post_article, name='post-article'),
    path('edit-article/<slug:slug>', views.edit_article, name='edit-article'),
    path('delete/<slug:slug>', views.delete_article, name='delete'),
    path('fave-add/<slug:slug>', views.favorite_article, name='fave-add'),
    path('detail/<slug:slug>', views.ArticleDetail.as_view(),
         name='article-detail'),
]
