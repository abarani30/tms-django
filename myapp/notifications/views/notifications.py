from django.shortcuts import render

def NotificationsView(request):
  template_name = "notifications.html"
  return render(request, template_name)