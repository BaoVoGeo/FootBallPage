from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^', include('intern.urls'), name='home'),
    url(r'^admin/', admin.site.urls),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.VENDORS_URL, document_root=settings.VENDORS_ROOT)
    
handler404 = 'intern.views.error'
