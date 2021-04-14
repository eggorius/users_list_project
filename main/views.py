from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .decorators import check_for_blocked_users
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


def block_users(users):
    group = Group.objects.get(name='blocked')
    for u in users:
        group.user_set.add(u)


def unblock_users(users):
    group = Group.objects.get(name='blocked')
    for u in users:
        group.user_set.remove(u)


@login_required(login_url='login')
@check_for_blocked_users
def index(request):
    if request.method == 'POST':
        selected = request.POST.getlist('chosen')
        selected_users = User.objects.filter(id__in=selected)
        if request.POST['action'] == 'delete':
            selected_users.delete()
        if request.POST['action'] == 'block':
            if request.user in selected_users:
                block_users(selected_users)
                return redirect('logout')
            block_users(selected_users)
        if request.POST['action'] == 'unblock':
            unblock_users(selected_users)
        users = User.objects.all()
        blocked = Group.objects.get(name='blocked')
        return render(request, 'main/index.html', {'users': users, 'blocked': blocked})

    blocked = Group.objects.get(name='blocked')
    users = User.objects.all()
    context = {
        'users': users,
        'blocked': blocked
    }
    return render(request, 'main/index.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
        return render(request, 'main/login.html', {'form': form})
    form = LoginForm(request.POST or None)
    return render(request, 'main/login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            # new_user.username = form.cleaned_data['username']
            # new_user.email = form.cleaned_data['email']
            # new_user.first_name = form.cleaned_data['first_name']
            # new_user.last_name = form.cleaned_data['last_name']
            # new_user.save()
            # new_user.set_password(form.cleaned_data['password'])
            # new_user.save()
            #
            # user = authenticate(request.POST)
            login(request, new_user)
            return redirect('home')
        return render(request, 'main/registration.html', {'form': form})
    form = RegistrationForm(request.POST or None)
    return render(request, 'main/registration.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
