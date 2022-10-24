from tempfile import template
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

def loginUser(request):
    if request.user.is_authenticated:
      return redirect("/")  
    if 'loginBtn' in request.POST:
      username = request.POST.get("username")
      password = request.POST.get("password")   
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect("/")    
      return render(request, "login.html", {"errMsg": "لقد فشلت عملية تسجيل الدخول"})   
    return render(request, 'login.html')


def logoutUser(request):
  logout(request)
  return redirect("/accounts/login/")