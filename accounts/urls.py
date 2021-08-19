from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='accounts'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('register/activate/<uidb64>/<token>',views.activate, name='activate'),
    
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password')
]