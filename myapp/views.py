from django.shortcuts import render
from django.views import View
from myapp.models import Profile, Task, Notification

class HomePageView(View):
  template_name = "index.html"

  def get(self, request):
    profile = Profile.objects.all()
    task    = Task.objects.prefetch_related("employees")
    notification = Notification.objects.prefetch_related("emps")
    if task and notification:
      return render(request, self.template_name, 
        {
          "profile": profile[0],
          "total_tasks": task[0].total_staff_tasks,
          "total_achieved": task[0].total_achieved_tasks,
          "total_unachieved": task[0].total_unachieved_tasks,
          "unreadable": task[0].unread_employee_tasks(request),
          "unreadable_staff": notification[0].unread_staff_notifications(request),
          "task": task[0]
        }
      )

    return render(request, self.template_name, 
      {
        "profile": profile[0],
        "total_tasks": 0,
        "total_achieved": 0,
        "total_unachieved": 0,
        "unreadable": 0,
        "unreadable_staff": 0,
        "task": 0,
      }
    )