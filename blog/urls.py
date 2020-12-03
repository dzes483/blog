"""coffeelover URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from blog import views

urlpatterns = [
    path('', views.ArticleList.as_view(), name='home'),
    path('blog/<str:slug>/', views.article_detail,
         name='article_detail'),
    path('blog/<str:slug>/update/',
         views.update_article, name='update_article'),
    path('blog/create/', views.ArticleCreateView.as_view(),
         name='article_create'),
    path('blog/<str:slug>/delete/',
         views.ArticleDeleteView.as_view(),
         name='delete_article'),
    path('blog/<str:slug>/comment/<int:pk>/delete',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
]
