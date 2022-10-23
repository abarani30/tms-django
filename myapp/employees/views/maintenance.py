from django.shortcuts import render

def MaintenanceEmployeesView(request):
    template_name = "maintenance_employees.html"
    return render(request, template_name)