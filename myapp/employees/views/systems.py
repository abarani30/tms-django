from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User

class SystemsEmployeesView(View):
  template_name = "systems_employees.html"

  def get(self, request):
    # get all the employees according to their division
    employees = [user for user in User.objects.all().select_related("profile") if request.user.profile.division == user.profile.division and user.is_active]
    return render(request, self.template_name, {"employees": employees})