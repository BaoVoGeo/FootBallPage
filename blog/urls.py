from django.conf.urls import url,include
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.show_blog, name='blog'),
    path('<int:pk>', views.post, name='post'),   #nen them slug truoc pk
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('like/<int:pk>', views.like_post, name='like_post'),
    path('dislike/<int:pk>', views.dislike_post, name='dislike_post'), 
    path('share/<int:pk>', views.share_post, name='share_post'),
    path('rate_post/<int:pk>', views.rate_post, name='rate_post'),
    
    # Tags
    url(r'^blog/(?P<slug>[-\w]+)/$', views.ListViewLeague.as_view(), name="tagged_books"),
    
    
]