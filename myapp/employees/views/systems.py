from django.shortcuts import render

def SystemsEmployeesView(request):
  template_name = "systems_employees.html"
  return render(request, template_name)