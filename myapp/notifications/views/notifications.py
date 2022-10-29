from django.shortcuts import render
from django.views import View
from myapp.models import Notification

class NotificationsView(View):
  template_name = "notifications.html"

  def get(self, request):
    notification = Notification.objects.prefetch_related("emps")
    return render(request, self.template_name, 
      { 
        "total": notification[0].countTotalNotifications(request),
        "unreadable": notification[0].countUnreadableNotifications(request),
        "all_notifications": notification[0].getUserNotifications(request)
      }
    )