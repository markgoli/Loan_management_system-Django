from django import forms
from django.contrib.auth.forms import UserCreationForm
from loan_products.models import LoanProduct
from django.contrib.auth.models import User

class LoanProductForm(forms.ModelForm):
    class Meta:
        model = LoanProduct
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required. Enter your phone number.')
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=True, help_text='Required. Select your gender.')
 
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'password1', 'password2']