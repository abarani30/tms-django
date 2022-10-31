from django.shortcuts import HttpResponseRedirect, render
from myapp.models import Task
import datetime
from typing import List

def get_all_notifications(request):
  task = Task.objects.prefetch_related("employees")
  if task:
    return render(request, "notifications.html", 
      { 
        "total": task[0].total_employee_tasks(request),
        "unreadable": task[0].unread_employee_tasks(request),
        "all_notifications": task[0].get_employee_tasks
      }
    )
  return HttpResponseRedirect("/notifications/")