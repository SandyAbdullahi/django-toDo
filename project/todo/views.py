
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import ListForm
from .models import List


def LANDING(request):
    count = User.objects.count()
    context = {
        'count': count
    }
    return render(request, 'pages/landing.html', context)

def ABOUT(request):
    return render(request, 'pages/about.html')


def NEW_USER(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form.clean()
            return redirect('login')
    else:
        form = UserCreationForm()
        context = {
            'form': form
        }
    return render(request, 'registration/sign_up.html', context)


@login_required
def DASHBOARD(request):
    user = request.user
    user_id = user.id
    if request.method == 'POST':
        new_list_form = ListForm(request.POST)
        if new_list_form.is_valid():
            new_list_form.save()
            new_list_form.clean()
            return redirect('dashboard')
    else:
        new_list_form = ListForm(initial={"user":user_id})



    context = {
        'form': new_list_form
    }
    return render(request, 'pages/dashboard.html', context)

@login_required
def UPDATE_LIST(request, list_id):
    list_id = int(list_id)
    try:
        selected_list = List.objects.get(id = list_id)
    except List.DoesNotExist:
        return redirect('dashboard')
    list_form = ListForm(request.POST or None, instance = selected_list)     
    if list_form.is_valid():
        list_form.save()
        list_form.clean()
        return redirect('dashboard')
    context = {
        'form': list_form
    }
    return render(request, 'pages/list_view.html', context)

def DELETE_LIST(request, list_id):
    list_id = int(list_id)
    try:
        selected_list = List.objects.get(id = list_id )
    except List.DoesNotExist:
        return redirect('landing')
    selected_list.delete()
    return redirect('dashboard')