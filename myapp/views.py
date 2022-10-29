from django.shortcuts import render
from django.views import View
from myapp.models import Profile, Task, Notification

class HomePageView(View):
  template_name = "index.html"

  def get(self, request):
    profile = Profile.objects.all()
    task    = Task.objects.prefetch_related("employees")
    notification = Notification.objects.prefetch_related("emps")
    return render(request, self.template_name, 
      {
        "profile": profile[0],
        "task": task[0],
        "unreadable": notification[0].countUnreadableNotifications(request)
      }
    )
