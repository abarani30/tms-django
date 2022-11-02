from django.shortcuts import render
from myapp.models import Notification
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from typing import List
from django.contrib.auth.models import User

# get request
@user_passes_test(lambda user: user.is_superuser)
def get_all_director_tasks(request) -> HttpResponse:
  if get_all_tasks() != []:
    return render(request, "director_tasks.html", context = get_context(request, get_all_tasks()))
  return render(request, "director_tasks.html", context = default_context())



# post request
@user_passes_test(lambda user: user.is_superuser)
def create_task_to_staff(request):
  return HttpResponseRedirect("/tasks/director/create/")





# get all the director tasks
def get_all_tasks() -> List[dict]:
  return list(Notification.objects.prefetch_related("emp"))



# get the context dictionary
def get_context(request, tasks):
  return {
    "admins": get_all_staff(),
    "tasks": tasks,
  }



# in case when there is no notifications to return
def default_context():
  return {
    "admins": get_all_staff(),
    "tasks": "[]",
  }



# get all the staff user (not superusers)
def get_all_staff() -> List[dict]:
  return [
    user for user in User.objects.all().select_related("profile") 
    if user.is_staff and not user.is_superuser
  ]
