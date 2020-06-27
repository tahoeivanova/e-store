from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from store.models import Customer

# Create your views here.
# @login_required(login_url='login')
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = CreateUserForm()
    context = {'form':form}

    if request.method =="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            Customer.objects.get_or_create(user=user, name=user.username, email=user.email)
            return redirect('login')
    return render(request, 'user/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'user/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')