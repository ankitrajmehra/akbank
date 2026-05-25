from django.shortcuts import render, redirect
from .models import user, BankAccount, Loan, Transaction, Suggestion

# ─── PUBLIC PAGES ───────────────────────────────────────

def index(req):
    return render(req, 'bank/index.html')

def about(req):
    return render(req, 'bank/about.html')

def services(req):
    return render(req, 'bank/services.html')

def contact(req):
    if req.method == 'POST':
        return render(req, 'bank/contact.html', {'success': True})
    return render(req, 'bank/contact.html')

def suggestion(req):
    success = False
    if req.method == 'POST':
        Suggestion.objects.create(
            name=req.POST.get('name', ''),
            email=req.POST.get('email', ''),
            category=req.POST.get('category', ''),
            rating=req.POST.get('rating', ''),
            message=req.POST.get('message', '')
        )
        success = True
    return render(req, 'bank/suggestion.html', {'success': success})

# ─── AUTH ────────────────────────────────────────────────

def signup(req):
    if req.method == 'POST':
        email = req.POST.get('email', '')
        password = req.POST.get('password', '')
        if user.objects.filter(email=email).exists():
            return render(req, 'bank/signup.html', {
                'error': 'Ye email already registered hai! Login karein.'
            })
        user.objects.create(email=email, password=password)
        return redirect('bank:signin')
    return render(req, 'bank/signup.html')

def signin(req):
    if req.method == 'POST':
        email = req.POST.get('email', '')
        password = req.POST.get('password', '')
        data = user.objects.filter(email=email, password=password)
        if data.exists():
            req.session['user_id'] = data[0].id
            req.session['user_name'] = data[0].email
            has_account = BankAccount.objects.filter(user_id=data[0].id).exists()
            if has_account:
                return redirect('bank:index')
            else:
                return redirect('bank:account')
        else:
            return render(req, 'bank/signin.html', {
                'error': 'Invalid Email or Password!'
            })
    return render(req, 'bank/signin.html')

def logout(req):
    req.session.flush()
    return redirect('bank:signin')

# ─── DASHBOARD ───────────────────────────────────────────

def account(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')
    user_id = req.session['user_id']
    existing_account = BankAccount.objects.filter(user_id=user_id).first()
    if req.method == 'POST':
        account_no = req.POST.get('account_no', '')
        name = req.POST.get('name', '')
        account_type = req.POST.get('account_type', '')
        branch = req.POST.get('branch', '')
        BankAccount.objects.create(
            user_id=user_id,
            account_no=account_no,
            name=name,
            account_type=account_type,
            branch=branch,
            balance=0
        )
        return redirect('bank:balance')
    return render(req, 'bank/account.html', {
        'existing_account': existing_account
    })

def deposit(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')
    user_id = req.session['user_id']
    acc = BankAccount.objects.filter(user_id=user_id).first()
    if not acc:
        return redirect('bank:account')
    if req.method == 'POST':
        amount = int(req.POST.get('amount', 0))
        acc.balance += amount
        acc.save()
        Transaction.objects.create(
            user_id=user_id,
            account=acc,
            transaction_type='deposit',
            amount=amount,
            balance_after=acc.balance
        )
        return redirect('bank:transaction')
    return render(req, 'bank/deposit.html', {'account': acc})

def withdraw(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')
    user_id = req.session['user_id']
    acc = BankAccount.objects.filter(user_id=user_id).first()
    if not acc:
        return redirect('bank:account')
    if req.method == 'POST':
        amount = int(req.POST.get('amount', 0))
        if amount > acc.balance:
            return render(req, 'bank/withdraw.html', {
                'account': acc,
                'error': '⚠️ Insufficient Balance!'
            })
        acc.balance -= amount
        acc.save()
        Transaction.objects.create(
            user_id=user_id,
            account=acc,
            transaction_type='withdraw',
            amount=amount,
            balance_after=acc.balance
        )
        return redirect('bank:transaction')
    return render(req, 'bank/withdraw.html', {'account': acc})

def balance(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')
    user_id = req.session['user_id']
    current_user = user.objects.get(id=user_id)
    accounts = BankAccount.objects.filter(user_id=user_id)
    return render(req, 'bank/balance.html', {
        'accounts': accounts,
        'current_user': current_user
    })

def loan(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')
    user_id = req.session['user_id']
    current_user = user.objects.get(id=user_id)
    acc = BankAccount.objects.filter(user_id=user_id).first()
    my_loans = Loan.objects.filter(user_id=user_id)
    if not acc:
        return redirect('bank:account')
    if req.method == 'POST':
        Loan.objects.create(
            user_id=user_id,
            account=acc,
            loan_type=req.POST.get('loan_type', ''),
            amount=int(req.POST.get('amount', 0)),
            duration_months=int(req.POST.get('duration_months', 0)),
            purpose=req.POST.get('purpose', ''),
            status='pending'
        )
        return redirect('bank:loan')
    return render(req, 'bank/loan.html', {
        'my_loans': my_loans,
        'account': acc,
        'current_user': current_user
    })

def transaction(req):
    if not req.session.get('user_id'):
        return redirect('bank:signin')
    user_id = req.session['user_id']
    current_user = user.objects.get(id=user_id)
    acc = BankAccount.objects.filter(user_id=user_id).first()
    transactions = Transaction.objects.filter(
        user_id=user_id
    ).order_by('-date')
    return render(req, 'bank/transaction.html', {
        'transactions': transactions,
        'account': acc,
        'current_user': current_user
    })