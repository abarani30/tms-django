from cProfile import Profile
from django.shortcuts import render
from django.views import View

class SystemsEmployeesView(View):
  template_name = "systems_employees.html"

  def get(self, request):
    profile = Profile.objects.all()
    return render(request, self.template_name, {"profile": profile[0]})