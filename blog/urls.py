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
    path('laliga/',views.show_blog_laliga, name ='blog_laliga')
]