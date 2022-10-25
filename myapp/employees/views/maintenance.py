from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User

class MaintenanceEmployeesView(View):
  template_name = "maintenance_employees.html"

  def get(self, request):
    return render(request, self.template_name, {"employees": self.getAllUsers()})

  def getAllUsers(self):
    return [user for user in User.objects.all().select_related("profile") if user.profile.division == "الفنية" and user.is_active]