from django.shortcuts import render

def DirectorTasksView(request):
    template_name = "director_tasks.html"
    return render(request, template_name)