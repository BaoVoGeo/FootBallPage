from django.conf.urls import url,include

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^', include('blog.urls'), name='index'),
    
    url('blog/',include('blog.urls'), name = 'showblog'),
    
    path('logout/',auth_views.LogoutView.as_view(next_page='/blog/'),name='logout'),
    path('profile/', views.profile, name = 'profile'),
    
    url('profile/change_info', views.fileUploaderView, name='fileUpLoaderView'),
    
    path('accounts/', include('accounts.urls'), name = 'accounts'),

    path('submit_review/', views.submit_review, name='submit_review'),
    
    path('search/', views.search, name = 'search'),

]