from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from notify import settings
from songs.views import CustomErrorPage
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('songs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),

handler502 = CustomErrorPage
handler503 = CustomErrorPage
handler408 = CustomErrorPage
handler407 = CustomErrorPage
handler404 = CustomErrorPage
handler403 = CustomErrorPage
handler401 = CustomErrorPage
