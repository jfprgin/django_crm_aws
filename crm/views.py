import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm, UpdateRecordForm, CreateRecordForm

LAMBDA_API_URL = settings.LAMBDA_API_URL

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
    url = LAMBDA_API_URL + "records"

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        messages.error(request, f"Could not fetch records: {e}")
        data = []

    return render(request, 'crm/dashboard.html', {'records': data})

# Crate Record using AWS Lambda
@login_required(login_url='my-login')
def create_record(request):
    url = LAMBDA_API_URL + "create"

    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            record_data = form.cleaned_data

            try:
                response = requests.post(url, json=record_data)
                if response.status_code == 200:
                    messages.success(request, 'Record created via Lambda!')
                else:
                    messages.error(request, 'Lambda error: ' + response.text)
            except Exception as e:
                messages.error(request, f'Error calling Lambda: {e}')

            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'crm/create-record.html', context)

# Update Record
@login_required(login_url='my-login')
def update_record(request, pk):
    url = f"{LAMBDA_API_URL}records/{pk}"

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST)

        if form.is_valid():
            record_data = form.cleaned_data

            try:
                response = requests.put(url, json=record_data)
                if response.status_code == 200:
                    messages.success(request, "Updated successfully")
                else:
                    messages.error(request, f"Failed: {response.text}")
            except Exception as e:
                messages.error(request, str(e))

            return redirect('dashboard')

    # Fetch current data to pre-fill the form
    response = requests.get(url)
    data = response.json()
    form = UpdateRecordForm(initial=data)

    return render(request, 'crm/update-record.html', {'form': form})

# Read / View a singular Record
@login_required(login_url='my-login')
def singular_record(request, pk):
    url = f"{LAMBDA_API_URL}records/{pk}"

    try:
        response = requests.get(url)
        record = response.json()
    except Exception as e:
        messages.error(request, f"Error fetching record: {e}")
        record = {}

    return render(request, 'crm/view-record.html', {'record': record})

# Delete Record
@login_required(login_url='my-login')
def delete_record(request, pk):
    url = f"{LAMBDA_API_URL}records/{pk}"

    try:
        response = requests.delete(url)
        if response.status_code == 200:
            messages.success(request, "Record deleted successfully")
        else:
            messages.error(request, f"Delete failed: {response.text}")
    except Exception as e:
        messages.error(request, str(e))

    return redirect('dashboard')

# Logout
def user_logout(request):
    auth.logout(request)

    messages.success(request, 'You have been logged out!')

    return redirect('my-login')
