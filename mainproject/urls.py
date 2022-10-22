from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings

if settings.DEBUG:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("", include('account.urls')),
        path("tasks/", include('task.urls')),
        path("notifications/", include("notification.urls"))
    ]
