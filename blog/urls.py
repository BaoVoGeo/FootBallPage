from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_blog, name='blog'),
    path('<int:pk>', views.post, name='post'),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('like/<int:pk>', views.like_post, name='like_post'),
    path('dislike/<int:pk>', views.dislike_post, name='dislike_post'), 
    path('share/<int:pk>', views.share_post, name='share_post'),
    path('la-liga/',views.show_blog_laliga, name ='blog_laliga'),
    path('premier-league/', views.show_blog_premier_league, name = 'blog_premier_league'),
    path('ligue-1/',views.show_blog_ligue_1, name ='blog_ligue1'),
    path('bundesliga/',views.show_blog_bundesliga, name ='blog_bundesliga'),
    path('serie-a/',views.show_blog_serie_A, name ='blog_seriea'),
    path('vietnam/',views.show_blog_vietnam, name ='blog_vietnam'),
    path('video/',views.show_blog_video, name ='blog_video'),
    path('football/',views.show_blog_football, name ='blog_football'),
    path('transform/',views.show_blog_transform, name ='blog_transform'),
    
]