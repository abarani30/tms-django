from django.shortcuts import HttpResponseRedirect, render
from myapp.models import Task

def get_all_notifications(request):
  if task_instance():
    return render(request, "notifications.html", context=get_context(request, task_instance()))
  return HttpResponseRedirect("/notifications/")



# get the task instance
def task_instance():
  return Task.objects.prefetch_related("employees")


# get the context dictionary
def get_context(request, task):
  return { 
    "total": task[0].total_employee_tasks(request),
    "unreadable": task[0].unread_employee_tasks(request),
    "all_notifications": task[0].get_employee_tasks(request)
  }