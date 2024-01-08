from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Allocation, CollectorReport, User, ClientRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from .forms import CollectorReportForm, ReportForm, ReportForm2, UserEditForm  
# import stripe
from django.conf import settings

# stripe.api_key = settings.STRIPE_SECRET_KEY

current_username = None

def homePage(request):
    if request.user.is_authenticated:
        current_username = request.user.username
        # Do something with the username, such as passing it to a template
        return render(request, 'index.html', {'current_username': current_username})
    else:
        # User is not authenticated, handle accordingly
        return render(request, 'index.html', {'current_username': None})




def RegisterPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        fullname = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        mobile_number = request.POST['mobile_number']
        print(request)
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, ': Username is already taken. Please choose a different one.')
            return redirect('register')

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, ': Email is already registered. Please use a different email.')
            return redirect('register')

        # If username and email are unique, create a new user
        user = User.objects.create_user(username=username, fullname=fullname, email=email, password=password, mobile_number=mobile_number)
        user.save()

        # messages.success(request, ': Registration successful. Please log in.')
        return redirect('login')  # Redirect to your login page

    return render(request, 'register.html')


def LoginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                # messages.success(request, ': Login successful.')
                return redirect('home')  # Redirect to your home or dashboard page
            else:
                messages.error(request, ': Invalid username or password. Please try again with correct creditionals.')
        else:
            messages.error(request, ': Invalid username or password. Please try again with correct creditionals.')
    else:
        form = AuthenticationForm(request)
    print(request)
    return render(request,"login.html")

@login_required(login_url='login') 
def user_logout(request):
    logout(request)
    return redirect('home')   


@login_required(login_url='login') 
def ClientRequestFunc(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        type_of_waste = request.POST.get('type_of_waste')

        if location and type_of_waste:
            client_request = ClientRequest.objects.create(
                user=request.user,  # Assuming the user is logged in
                location=location,
                type_of_waste=type_of_waste
            )
            # messages.success(request, 'Request submitted successfully!')
            return redirect('home')  # Redirect to a success page or any other page
        else:
            messages.error(request, 'Error in the form submission. Please check the fields.')


    return render(request, 'ComplaintForm.html')

@login_required(login_url='login') 
def report(request):
    return render(request, 'report.html')

@login_required(login_url='login') 
def admin_page(request):
    users = User.objects.all()
    requests = ClientRequest.objects.all().order_by('-timestamp')
    allocations = Allocation.objects.all().order_by('-timestamp')
    reports = CollectorReport.objects.all().order_by('-timestamp')
    return render(request, 'admin.html', {'users': users, 'requests':requests, 'allocations':allocations, 'reports':reports})


@login_required(login_url='login') 
def allot_request(request):
    if request.method == 'POST':
        collector_id = request.POST.get('collector')
        request_id = request.POST.get('request')
        
        if collector_id and request_id:
            collector = User.objects.get(pk=collector_id)
            client_request = ClientRequest.objects.get(pk=request_id)
            
            # Check if the request is already allotted
            if client_request.alloted:
                messages.error(request, 'Request already allotted.')
            else:
                # Allot the request to the collector
                Allocation.objects.create(collector=collector, client_request=client_request)
                client_request.alloted = True
                client_request.save()
                # messages.success(request, 'Request successfully allotted.')
                return redirect('admin_page')  # Redirect to the page displaying all requests

    # Fetch collectors and client requests to populate the form
    collectors = User.objects.filter(collector=True)
    requests = ClientRequest.objects.filter(alloted=False)

    return render(request, 'allocate_request.html', {'collectors': collectors, 'requests': requests})

@login_required(login_url='login') 
def edit_user(request, user_id):
    user1 = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user1)  # Fix: Change 'user' to 'user1'
        if form.is_valid():
            form.save()
            return redirect('admin_page') 
    else:
        form = UserEditForm(instance=user1)  # Fix: Change 'user' to 'user1'

    return render(request, 'edit_user.html', {'form': form, 'user1': user1})





# views.py
def submit_report(request, request_id):
    if request.method == 'POST':
        form = ReportForm(request_id, request.POST, collector=request.user)
        if form.is_valid():
            report = form.save(commit=False)
            report.collector = request.user
            report.save()
            return redirect('reports')  # Redirect to the page that displays reports
    else:
        form = ReportForm(request_id, collector=request.user)

    return render(request, 'submit_report.html', {'form': form})





def reports(request):
    collector_reports = CollectorReport.objects.filter(collector=request.user)
    allocations = Allocation.objects.filter(collector=request.user)
    requests_without_report = []
    for alloc in allocations: 
        # Use get() instead of first(), and filter with client_request_id
        requests_report = CollectorReport.objects.filter(client_request=alloc.client_request).first()

        if not requests_report:
            request_of_client = ClientRequest.objects.get(id=alloc.client_request.id)
            requests_without_report.append(request_of_client)

    context = {
        'requests_without_report': requests_without_report,
        'collector_reports': collector_reports
    }
    return render(request, 'report.html', context)



@login_required(login_url='login') 
def Status(request):
    requests = ClientRequest.objects.filter(user=request.user).order_by('-timestamp')
    requested_with = []
    for r in requests:
        allocated = Allocation.objects.filter(client_request=r.id).first()
        if allocated:
            collector = User.objects.get(id=allocated.collector.id)
            requested_with.append([r,collector])
        else:
            collector=None
            requested_with.append([r,collector])
        print(requested_with)
    return render(request, 'status.html', {'requests': requested_with})

def update_report(request, report_id):
    report = get_object_or_404(CollectorReport, id=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if report.confirmation_from_client:
            form = ReportForm2(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('reports')  # Redirect to the report page after updating
    else:
        if report.confirmation_from_client:
            form = ReportForm2(instance=report)
            # return redirect('submit_report')
        else:
            form = ReportForm(instance=report)

    return render(request, 'updateForm.html', {'form': form, 'report': report})

def report_details(request, report_id):
    report = CollectorReport.objects.filter(client_request=report_id)
    if not report:
        return redirect('status')
    report = get_object_or_404(CollectorReport, client_request=report_id)
    return render(request, 'report_details.html', {'report': report})

def confirm_report(request, report_id):
    try:
        report = CollectorReport.objects.get(id=report_id)
    except CollectorReport.DoesNotExist:
        raise Http404("Report does not exist")
    # Your logic here


    # Your logic to handle the confirmation

    report.confirmation_from_client = True
    report.save()

    return redirect('report_details', report_id=report_id)

def contact_us(request):
    return render(request, 'contact_us.htm')

def abc(request):
    return render(request,'abc.html')