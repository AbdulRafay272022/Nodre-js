# myapp/views.py
from django.shortcuts import render, redirect,get_list_or_404,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import ProspectForm, LoginForm, AddForm
from .models import Prospect, CustomUser


def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_active and u.admin)(view_func))
    return decorated_view_func

@login_required
def prospect_view(request):
    if request.method == 'POST':
        form = ProspectForm(request.POST)
        if form.is_valid():
            prospect = form.save(commit=False)
            prospect.user = request.user
            prospect.save()
            return redirect('success')
    else:
        form = ProspectForm()
    return render(request, 'form.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('prospect_form')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
#@admin_required 
def add_view(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('prospect_form')
    else:
        form = AddForm()
    return render(request, 'add.html', {'form': form})

def prospect_list_view(request):
    prospects = Prospect.objects.all()
    return render(request, 'prospect_list.html', {'prospects': prospects})

def prospect_edit_view(request, id):
    prospect = get_object_or_404(Prospect, id=id)
    if request.method == 'POST':
        form = ProspectForm(request.POST, instance=prospect)
        if form.is_valid():
            form.save()
            return redirect('prospect_list')
    else:
        form = ProspectForm(instance=prospect)
    return render(request, 'prospect_edit.html', {'form': form})

def prospect_delete_view(request, id):
    prospect = get_object_or_404(Prospect, id=id)
    if request.method == 'POST':
        prospect.delete()
        return redirect('prospect_list')
    return render(request, 'prospect_delete.html', {'prospect': prospect})