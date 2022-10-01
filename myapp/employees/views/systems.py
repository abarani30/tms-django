from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from myapp.models import Task
from django.template.response import SimpleTemplateResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# a view to handle the get request
def get_all_employees(request) -> SimpleTemplateResponse:
  if is_task():
    return render(request, "systems_employees.html", 
    context= get_context(request, is_task()))
  return render(request, "systems_employees.html", context = default_context()) 



# a view to handle the post request (register a new user)
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def register_user(request) -> HttpResponseRedirect:
  if request.method != "POST":
    return HttpResponseRedirect("/employees/systems/")
  
  if not validate_data(request): messages.error(request, "البيانات التي ارسلتها غير صحيحة")
  else: 
    update_profile(request, assign_role(request, add_user(request)))
    messages.success(request, "تم انشاء الحساب بنجاح")
  

  return HttpResponseRedirect("/employees/systems/")


# get the context dictionary
def get_context(request, task):
  return {
    "employees": get_all(),
    "unreadable": task[0].unread_employee_tasks(request)
  }



# in case when there is no employees in the this division
def default_context():
  return {
    "employees": "[]",
  }



# check if there is any tasks
def is_task():
  return Task.objects.prefetch_related("employees")



# get all the active employees in the same division
def get_all():
  return [user for user in User.objects.all().select_related("profile") if user.profile.division == "الانظمة" and user.is_active]



# validate the form inputs data
def validate_data(request) -> bool:
  # check if there is user associated with the username
  return bool(
    not is_username(request) and 
    request.POST.get("username") and 
    password_length(request) and 
    is_outlook_mail(request) and 
    is_role(request)
  )



# check if the username is exists or not
def is_username(request) -> bool:
  return bool(User.objects.filter(username=request.POST.get("username")).exists())



# password length should be more than six characters
def password_length(request) ->bool:
  return len(request.POST.get("password")) >= 6



# check if the email is outlook mail
def is_outlook_mail(request) -> bool:
  return "outlook.com" in request.POST.get("email")



# check if the current role is in the user roles
def is_role(request) -> bool:
  return request.POST.get("role") in ["ادمن", "مستخدم", "محرر"]



# create a new user with a hashed password
def add_user(request) -> User:
  return User.objects.create_user(
    username = request.POST.get("username"),
    password = request.POST.get("password"),
    email = request.POST.get("email")
  )



# assign a role to the newly created user
def assign_role(request, user) -> User:
  if request.POST.get("role") == "ادمن":
    user.is_staff = True
    user.save()
  return user



# update the user profile 
def update_profile(request, user) -> bool:
  user.profile.division = request.user.profile.division
  user.profile.account  = request.POST.get("role")
  user.save()
  return True