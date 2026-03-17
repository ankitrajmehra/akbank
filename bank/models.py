from django.db import models

class user(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.email

class BankAccount(models.Model):
    user = models.ForeignKey('user', on_delete=models.CASCADE, null=True)
    account_no = models.IntegerField()
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    balance = models.IntegerField()
    def __str__(self):
        return self.name

class Loan(models.Model):
    LOAN_TYPES = [
        ('home', 'Home Loan'),
        ('car', 'Car Loan'),
        ('personal', 'Personal Loan'),
        ('education', 'Education Loan'),
        ('business', 'Business Loan'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey('user', on_delete=models.CASCADE, null=True)
    account = models.ForeignKey('BankAccount', on_delete=models.CASCADE, null=True)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount = models.IntegerField()
    duration_months = models.IntegerField()
    purpose = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.loan_type} - {self.amount}"

# ← YE ADD KARO ✅
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    user = models.ForeignKey('user', on_delete=models.CASCADE, null=True)
    account = models.ForeignKey('BankAccount', on_delete=models.CASCADE, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.IntegerField()
    balance_after = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

# ← YE BHI ADD KARO ✅
class Suggestion(models.Model):
    CATEGORY_CHOICES = [
        ('service', 'Service'),
        ('loan', 'Loan'),
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('website', 'Website'),
        ('other', 'Other'),
    ]
    RATING_CHOICES = [
        ('5', '⭐⭐⭐⭐⭐ Excellent'),
        ('4', '⭐⭐⭐⭐ Good'),
        ('3', '⭐⭐⭐ Average'),
        ('2', '⭐⭐ Poor'),
        ('1', '⭐ Very Poor'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    rating = models.CharField(max_length=2, choices=RATING_CHOICES)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.category}"