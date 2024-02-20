from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from loan_products.models import LoanProduct

class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]

    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='pending')
    loan_date = models.DateField()
    applied_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_principal_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_interest_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_penalties_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
    late_payment_penalties = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attachment = models.FileField(upload_to='loan_attachments/', null=True, blank=True)
    approved_date = models.DateField(blank=True, null=True, default=None)
    approved_by =  models.ForeignKey(User, on_delete=models.CASCADE,related_name='approved_by', blank=True, null=True)
    description = models.TextField(blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f'{self.borrower.username} - {self.loan_product.product_name}'

    class Meta:
        db_table = "loans"


class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    repayment_date = models.DateField()
    principal_paid = models.DecimalField(max_digits=10, decimal_places=2)
    interest_paid = models.DecimalField(max_digits=10, decimal_places=2)
    penalties_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Repayment for Loan {self.loan.id} on {self.repayment_date}"
    
    class Meta:
        db_table = "loan_repayments"





