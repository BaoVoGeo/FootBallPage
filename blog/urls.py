from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_blog, name='blog'),
    path('<int:pk>', views.post, name='post'),
    path('accounts/', include('accounts.urls'), name='accounts')
]