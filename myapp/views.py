from django.shortcuts import render
from django.views import View
from myapp.models import Profile, Task

class HomePageView(View):
  template_name = "index.html"

  def get(self, request):
    profile = Profile.objects.all()
    task    = Task.objects.prefetch_related("employees")
    return render(request, self.template_name, 
      {
        "profile": profile[0],
        "task": task[0],
      }
    )
