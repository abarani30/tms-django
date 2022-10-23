from django.shortcuts import render

def SystemTasksView(request):
  template_name = "systems_tasks.html"
  return render(request, template_name)