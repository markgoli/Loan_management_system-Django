from django.db import models


class LoanProduct(models.Model):
    INTEREST_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('variable', 'Variable'),
    ]

    TERM_PERIOD_CHOICES = [
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    minimum_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    maximum_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_rate_per_year = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    interest_type = models.CharField(max_length=10, choices=INTEREST_TYPE_CHOICES, default='fixed')
    max_term = models.IntegerField(default=0)
    term_period = models.CharField(max_length=10, choices=TERM_PERIOD_CHOICES, default='months')
    late_payment_penalties = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = "loan_product"


