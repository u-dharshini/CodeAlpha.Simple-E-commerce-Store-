from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # After login go to homepage
        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})
    return render(request, "accounts/login.html")
    

def home_view(request):
    return render(request, "accounts/home.html")

