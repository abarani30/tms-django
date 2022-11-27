from typing import List, Dict
from django.shortcuts import HttpResponseRedirect, render
from myapp.models import Notification, Task
from django.contrib.auth.decorators import user_passes_test


# get all the notifications for employees
def get_all_notifications(request):
  if task_instance() and notification_instance():
    return render(request, "notifications.html", context=get_context(request, task_instance(), notification_instance()))
  return render(request, "notifications.html", context=get_context(request, 0, 0))



# get the task instance
def task_instance():
  return Task.objects.prefetch_related("employees")


# get the notification instance
def notification_instance():
  return Notification.objects.prefetch_related("emps")



# get all the notifications created by the superuser
@user_passes_test(lambda user: user.is_staff)
def get_all_superuser_notifications(request):
  return [
    notification 
    for notification in Notification.objects.prefetch_related("emps").all()
    if request.user in notification.emps.all()
  ]



# receive the notification by the staff user
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def receive_notification(request, id: int) -> HttpResponseRedirect:
  if len(get_notification(id)) != 0 and staff_notified(request, id):
    update_received_field(get_notification(id)[0])
  return HttpResponseRedirect('/notifications/')



# get the current task by id
def get_notification(id: int) -> List[dict]:
    return Notification.objects.filter(pk=id).prefetch_related("emps")



# check if the staff in the notification list (is notified)
def staff_notified(request, id: int) -> bool:
    return request.user in get_notification(id)[0].emps.all()



# update the current task received
def update_received_field(notification: Dict):
    if not notification.received:
        notification.received = True
        notification.save()
        return True
    return False



# get the context dictionary
def get_context(request, task, notification):
  if task != 0:
    return { 
      "unreadable": task[0].unread_employee_tasks(request),
      "unreadable_staff": notification[0].unread_staff_notifications(request),
      "all_notifications": task[0].get_employee_tasks(request),
      "superuser_notifications": get_all_superuser_notifications(request),
    }
  return { 
    "unreadable": 0,
    "unreadable_staff": 0,
    "all_notifications": 0,
    "superuser_notifications": 0,
  }