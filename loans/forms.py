# forms.py
from django import forms
from .models import Loan, LoanRepayment
from loan_products.models import LoanProduct

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loan_product', 'applied_amount', 'description']


    def clean(self):
        cleaned_data = super().clean()
        loan_product = cleaned_data.get("loan_product")
        applied_amount = cleaned_data.get("applied_amount")

        if loan_product and (applied_amount < loan_product.minimum_amount or applied_amount > loan_product.maximum_amount):
            raise forms.ValidationError("Applied amount must be within the allowed range.")

        return cleaned_data

class LoanApprovalForm(forms.Form):
    APPROVAL_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    approval_status = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect)
    remarks = forms.CharField(widget=forms.Textarea, required=False)

class LoanRepaymentForm(forms.ModelForm):
    class Meta:
        model = LoanRepayment
        fields = ['principal_paid', 'interest_paid', 'penalties_paid', 'remarks','repayment_date']

