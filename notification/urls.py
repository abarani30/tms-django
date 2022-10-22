from django.urls import path
from notification.views import notification

urlpatterns = [
  path("", notification.NotificationsView, name="notifications_page")
]