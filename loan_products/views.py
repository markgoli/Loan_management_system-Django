from django.shortcuts import render, redirect, get_object_or_404
from loan_products.forms import LoanProductForm
from loan_products.models import LoanProduct
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from user_details.models import UserDetail
from loans.models import Loan
from django.db import models

# Create your views here.
def home(request):
    return render(request,'home.html')

@login_required(login_url='/login/')
def new_loan_product(request):
    if request.method == "POST":
        form = LoanProductForm(request.POST)
        if form.is_valid():
            try:
                # Save the form data to the database
                form.save()
                return redirect('/loan-products/')
            except ValidationError as e:
                # Handle validation errors
                messages.error(request, f"Validation error: {', '.join(e)}")
            except Exception as e:
                # Handle other exceptions
                messages.error(request, f"An error occurred: {e}")
    else:
        form = LoanProductForm()

    return render(request, 'new_loan_product.html', {'form': form})

def show(request):
    loan_products = LoanProduct.objects.all()
    user_details = UserDetail.objects.get(user_id=request.user)
    return render(request,"show.html",{'loan_products':loan_products, 'user_details': user_details})

@login_required(login_url='/login/')
def edit(request, id):
    # Retrieve the loan product or return a 404 response
    loan_product = get_object_or_404(LoanProduct, id=id)


    if request.method == "POST":
        form = LoanProductForm(request.POST, instance=loan_product)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Loan product updated successfully.")
                return redirect("/loan-products/")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
    else:
        form = LoanProductForm(instance=loan_product)

    return render(request, 'edit.html', {'loan_product': loan_product, 'form': form})

@login_required(login_url='/login/')
def destroy(request, id):
    loan_product = LoanProduct.objects.get(id=id)
    loan_product.delete()
    return redirect("/loan-products/")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_details = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'phone_number': request.POST.get('phone_number'),
                'gender': request.POST.get('gender'),
                'user_id': user
            }
            UserDetail.objects.create(**user_details)
            return redirect('loan_products')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('loan_products')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')

def set_session_token(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    response = HttpResponse()
    session_token = request.POST.get('session_token')
    response = HttpResponseRedirect('/')
    expires = datetime.now() + timedelta(days=7)
    response.set_cookie('sessionid', session_token, expires=expires, path='/')
    return response

def get_session_token(request):
    session_token = request.COOKIES.get('sessionid')
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if session_token:
        return render(request, 'authorized.html', {'session_token': session_token})

    return render(request, 'authorized.html', {'session_token': 'No session token set'})

@login_required(login_url='/login/')
def view_members(request):
    users = UserDetail.objects.all()
    return render(request, 'members.html', {'users': users})

@login_required(login_url='/login/')
def dashboard(request):
    user_details = UserDetail.objects.get(user_id=request.user)
    loans = Loan.objects.all()

    if user_details.is_admin:
        template = 'admin_dashboard.html'
        users_count = UserDetail.objects.count()
        loan_products_count = LoanProduct.objects.count()
        loans_count = Loan.objects.count()
        total_principal = Loan.objects.aggregate(models.Sum('applied_amount'))['applied_amount__sum']
        total_interest = Loan.objects.aggregate(models.Sum('total_interest_paid'))['total_interest_paid__sum']
        
        context = {
            'users_count': users_count,
            'loan_products_count': loan_products_count,
            'loans_count': loans_count,
            'total_principal': total_principal,
            'total_interest': total_interest,
            'loans': loans,
        }
    else:
        loans = Loan.objects.filter(borrower=request.user)
        template = 'user_dashboard.html'
        context = {
            'user_details': user_details,
            'user_loans': loans
        }
    
    return render(request, template, context)