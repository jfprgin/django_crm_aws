from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CreateUserForm, LoginForm, UpdateRecordForm, CreateRecordForm
from .models import Record


# Homepage
def home(request):

    return render(request, 'crm/index.html')

# Register
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Account created successfully! You can now log in.')

            return redirect('my-login')

    context = {'form': form}

    return render(request, 'crm/register.html', context)

# Login
def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect('dashboard')

    context = {'form': form}

    return render(request, 'crm/my-login.html', context)


# Dashboard
@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'crm/dashboard.html', context)

# Crate Record
@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Record created successfully!')

            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'crm/create-record.html', context)

# Update Record
@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()

            messages.success(request, 'Record updated successfully!')

            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'crm/update-record.html', context)

# Read / View a singular Record
@login_required(login_url='my-login')
def singular_record(request, pk):
    all_records = Record.objects.get(id=pk)

    context = {'record': all_records}

    return render(request, 'crm/view-record.html', context)

# Delete Record
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()

    messages.success(request, 'Record deleted successfully!')

    return redirect('dashboard')

# Logout
def user_logout(request):
    auth.logout(request)

    messages.success(request, 'You have been logged out!')

    return redirect('my-login')
