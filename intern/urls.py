from django.conf.urls import url,include

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('blog.urls'), name='index'),
    path('blog/',include('blog.urls'), name = 'showblog'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/blog/'),name='logout'),
    path('profile/', views.profile, name = 'profile'),
    path('profile/change_info', views.fileUploaderView, name='fileUpLoaderView'),
    path('accounts/', include('accounts.urls'), name = 'accounts'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('search/', views.SearchList.as_view(), name = 'search'),
    path('filter/', views.FilterList.as_view(), name = 'filter'),
]