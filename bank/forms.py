from django import forms
from .models import *

class UserForms(forms.ModelForm):
    class Meta:
        model=user
        fields='__all__'
#-----------------------------------------------------------------------

class UserForms(forms.ModelForm):
    class Meta:
        model = user
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Password'
            }),
        }

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = [
            'account_no',    # ← model mein hai ✅
            'name',          # ← model mein hai ✅
            'account_type',  # ← model mein hai ✅
            'branch',        # ← model mein hai ✅
            'balance',       # ← model mein hai ✅
        ]
        widgets = {
            'account_no': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Account Number'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Account Holder Name'
            }),
            'account_type': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g. Savings / Current'
            }),
            'branch': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Branch Name'
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Initial Balance'
            }),
        }
        #----------------------------------------------
class UserForms(forms.ModelForm):
    class Meta:
        model = user
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),
        }

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_no', 'name', 'account_type', 'branch', 'balance']
        widgets = {
            'account_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_type': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# ← YE ADD KARO ✅
class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loan_type', 'amount', 'duration_months', 'purpose']
        widgets = {
            'loan_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Loan amount (₹)'
            }),
            'duration_months': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in months (e.g. 12, 24, 36)'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Loan lene ka reason likho...'
            }),
        }
