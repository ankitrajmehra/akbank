from django.shortcuts import render, redirect
from .forms import *
from .models import *

def index(req):
    return render(req, 'bank/index.html')

def contact(req):
    return render(req, 'bank/contact.html')

def about(req):
    return render(req, 'bank/about.html')

def services(req):
    return render(req, 'bank/services.html')

def suggestion(req):
    success = False
    if req.method == 'POST':
        name = req.POST.get('name', '')
        email = req.POST.get('email', '')
        category = req.POST.get('category', '')
        rating = req.POST.get('rating', '')
        message = req.POST.get('message', '')

        # Database mein save karo ✅
        suggestion.objects.create(
            name=name,
            email=email,
            category=category,
            rating=rating,
            message=message
        )
        success = True

    return render(req, 'bank/suggestion.html', {'success': success})

def signup(req):
    if req.method == 'POST':
        form = UserForms(req.POST)
        if form.is_valid():
            form.save()
            return redirect('bank:signin')
        else:
            return redirect('bank:signup')
    else:
        form = UserForms()
    return render(req, 'bank/signup.html', {'form': form})

def signup(req):
    if req.method == 'POST':
        email = req.POST.get('email', '')
        password = req.POST.get('password', '')

        # Email already hai check karo
        if user.objects.filter(email=email).exists():
            return render(req, 'bank/signup.html', {
                'error': 'Ye email already registered hai! Login karein.'
            })

        # Naya user banao
        user.objects.create(email=email, password=password)
        return redirect('bank:signin')

    return render(req, 'bank/signup.html')
# ← YE ADD KARO ✅
def signin(req):
    if req.method == 'POST':
        email = req.POST.get('email', '')
        password = req.POST.get('password', '')
        data = user.objects.filter(email=email, password=password)
        if len(data) > 0:
            req.session['user_id'] = data[0].id
            req.session['user_name'] = data[0].email
            has_account = BankAccount.objects.filter(
                user_id=data[0].id
            ).exists()
            if has_account:
                return redirect('bank:index')
            else:
                return redirect('bank:account')
        else:
            return render(req, 'bank/signin.html', {
                'error': 'Invalid Email or Password!'
            })
    return render(req, 'bank/signin.html')
def account(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')
    
    user_id = req.session['user_id']
    existing_account = BankAccount.objects.filter(user_id=user_id).first()

    # ← Balance pe redirect mat karo — form dikhao ✅
    if req.method == 'POST':
        form = BankAccountForm(req.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = user_id
            f.save()
            return redirect('bank:balance')
    else:
        form = BankAccountForm()

    return render(req, 'bank/account.html', {
        'form': form,
        'existing_account': existing_account  # ← Dono cases handle ✅
    })

def deposit(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')

    user_id = req.session['user_id']
    account = BankAccount.objects.filter(user_id=user_id).first()

    if not account:
        return redirect('bank:account')

    if req.method == 'POST':
        amount = int(req.POST.get('amount', 0))
        account.balance += amount
        account.save()

        # ← YE LINE HAI KYA? ✅
        Transaction.objects.create(
            user_id=user_id,
            account=account,
            transaction_type='deposit',
            amount=amount,
            balance_after=account.balance
        )
        return redirect('bank:transaction')

    return render(req, 'bank/deposit.html', {'account': account})

def withdraw(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')

    user_id = req.session['user_id']
    account = BankAccount.objects.filter(user_id=user_id).first()

    if not account:
        return redirect('bank:account')

    if req.method == 'POST':
        amount = int(req.POST.get('amount', 0))

        if amount > account.balance:
            return render(req, 'bank/withdraw.html', {
                'account': account,
                'error': '⚠️ Insufficient Balance!'
            })

        account.balance -= amount
        account.save()

        # ← YE LINE HAI KYA? ✅
        Transaction.objects.create(
            user_id=user_id,
            account=account,
            transaction_type='withdraw',
            amount=amount,
            balance_after=account.balance
        )
        return redirect('bank:transaction')

    return render(req, 'bank/withdraw.html', {'account': account})

def balance(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')
    
    user_id = req.session['user_id']
    
    # Login user ki info
    current_user = user.objects.get(id=user_id)
    
    # Us user ke accounts
    accounts = BankAccount.objects.filter(user_id=user_id)
    
    return render(req, 'bank/balance.html', {
        'accounts': accounts,
        'current_user': current_user
    })

def loan(req):
    return render(req, 'bank/loan.html')
def logout(req):
    req.session.flush()  # Session clear ✅
    return redirect('bank:signin')
#-------------------------------------------------------------


def loan(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')

    user_id = req.session['user_id']
    current_user = user.objects.get(id=user_id)
    account = BankAccount.objects.filter(user_id=user_id).first()

    # Purane loans
    my_loans = Loan.objects.filter(user_id=user_id)

    if not account:
        return redirect('bank:account')

    if req.method == 'POST':
        form = LoanForm(req.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = user_id
            f.account = account
            f.status = 'pending'
            f.save()
            return redirect('bank:loan')
    else:
        form = LoanForm()

    return render(req, 'bank/loan.html', {
        'form': form,
        'my_loans': my_loans,
        'account': account,
        'current_user': current_user
    })
#---------------------------------------------------
def contact(req):
    if req.method == 'POST':
        # Form data save kar sakte ho
        name = req.POST.get('name')
        email = req.POST.get('email')
        message = req.POST.get('message')
        return render(req, 'bank/contact.html', {'success': True})
    return render(req, 'bank/contact.html')

#--------------------------------------------------------
def transaction(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')

    user_id = req.session['user_id']
    current_user = user.objects.get(id=user_id)
    account = BankAccount.objects.filter(user_id=user_id).first()

    # Saari transactions — latest pehle
    transactions = Transaction.objects.filter(
        user_id=user_id
    ).order_by('-date')

    return render(req, 'bank/transaction.html', {
        'transactions': transactions,
        'account': account,
        'current_user': current_user
    })