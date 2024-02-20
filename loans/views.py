from django.shortcuts import render, redirect,get_object_or_404
from .models import Loan, LoanRepayment  # Assuming your Loan model is named Loan
from django.contrib.auth.decorators import login_required
from loan_products.models import LoanProduct
from user_details.models import UserDetail
from datetime import datetime, timedelta
from decimal import Decimal
from .forms import LoanApplicationForm, LoanApprovalForm, LoanRepaymentForm  # Assuming you have a LoanApplicationForm

@login_required(login_url='/login/')
def apply_for_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.status = 'Pending'  # Set the initial status
            loan.borrower = request.user
            loan.loan_date = datetime.now()
            loan.save()
            return redirect('all_loans')  # Redirect to a success page
    else:
        form = LoanApplicationForm()
    
    loan_products = LoanProduct.objects.all()

    return render(request, 'apply_for_loan.html', {'form': form, 'loan_products': loan_products})

@login_required(login_url='/login/')
def all_loans(request):
    loans = []
    user_details = UserDetail.objects.get(user_id=request.user)
    if user_details.is_admin:
        loans = Loan.objects.all()
    else:
        loans = Loan.objects.filter(borrower=request.user)
    return render(request, 'all_loans.html', {'loans': loans, user_details: user_details})

@login_required(login_url='/login/')
def loan_detail(request, loan_id):
    user_details = UserDetail.objects.get(user_id=request.user)
    loan = get_object_or_404(Loan, id=loan_id)
    # collateral = Collateral.objects.filter(loan=loan).first()  # Assuming a one-to-one relationship


     # Retrieve the loan product based on the provided ID
    loan_product = LoanProduct.objects.get(pk=loan.loan_product.id)

    # Calculate the repayment schedule
    repayment_schedule = calculate_repayment_schedule(loan_product, loan.applied_amount, loan.loan_date)
    repayments = LoanRepayment.objects.filter(loan=loan).order_by('repayment_date')


    context = {
        'loan': loan,
        'repayment_schedule': repayment_schedule,
        'repayments': repayments,
        'user_details': user_details,
    }



    return render(request, 'loan_detail.html', context)

def loan_approval(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    if request.method == 'POST':
        form = LoanApprovalForm(request.POST)
        if form.is_valid():
            loan.status = form.cleaned_data['approval_status']
            loan.approved_date = datetime.now()
            loan.approved_by = request.user  # Assuming you're using User authentication
            loan.remarks = form.cleaned_data['remarks']
            loan.save()
            return redirect('all_loans') # Redirect to home or another page after approval

    else:
        form = LoanApprovalForm()

    return render(request, 'loan_approval.html', {'loan': loan, 'form': form})


def calculate_repayment_schedule(loan_product, loan_amount, loan_date):
    # Extract relevant details from the loan product
    interest_rate = loan_product.interest_rate_per_year / 100
    term_period = loan_product.term_period
    loan_amount = Decimal(loan_amount)
    installment_count = loan_product.max_term

    # Calculate monthly interest rate
    monthly_interest_rate = interest_rate / 12

    # Calculate monthly installment using the formula for monthly loan payment
    monthly_installment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-installment_count))

    # Initialize repayment schedule list
    repayment_schedule = []

    # Calculate remaining balance and interest for each installment
    remaining_balance = loan_amount
    for installment in range(1, installment_count + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_installment - interest_payment
        remaining_balance -= principal_payment

        # Append installment details to the schedule
        installment_date = loan_date + timedelta(days=(int(loan_product.max_term) * installment))
        repayment_schedule.append({
            'installment_number': installment,
            'installment_date': installment_date,
            'principal_payment': round(principal_payment),
            'interest_payment': round(interest_payment),
            'remaining_balance': round(remaining_balance),
        })

    return repayment_schedule



def create_loan_repayment(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    if request.method == 'POST':
        form = LoanRepaymentForm(request.POST)
        if form.is_valid():
            repayment = form.save(commit=False)
            repayment.loan = loan
            repayment.save()

            # Update loan details
            loan.total_principal_paid += repayment.principal_paid
            loan.total_interest_paid += repayment.interest_paid
            loan.save()
            loan.due_amount = loan.applied_amount - loan.total_principal_paid
            loan.save()

            return redirect('loan_detail', loan_id=loan.id)
    else:
        form = LoanRepaymentForm()

    return redirect('loan_detail', loan_id=loan.id)

def delete_repayment(request, loan_id, repayment_id):
    loan_repayment = get_object_or_404(LoanRepayment, id=repayment_id, loan__id=loan_id)

    loan_repayment.delete()
        # You may want to update the cumulative value of all payments here

    return redirect('loan_detail', loan_id=loan_id)

