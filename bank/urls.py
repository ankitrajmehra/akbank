from django.urls import path
from django.shortcuts import render

app_name = 'bank'


def home(request):
    return render(request, 'bank/index.html')


def signup(request):
    return render(request, 'bank/index.html')


def signin(request):
    return render(request, 'bank/index.html')


def logout(request):
    return render(request, 'bank/index.html')


def account(request):
    return render(request, 'bank/index.html')


def deposit(request):
    return render(request, 'bank/index.html')


def withdraw(request):
    return render(request, 'bank/index.html')


def balance(request):
    return render(request, 'bank/index.html')


def loan(request):
    return render(request, 'bank/index.html')


def transaction(request):
    return render(request, 'bank/index.html')


def about(request):
    return render(request, 'bank/index.html')


def contact(request):
    return render(request, 'bank/index.html')


def services(request):
    return render(request, 'bank/index.html')


def suggestion(request):
    return render(request, 'bank/index.html')


urlpatterns = [

    path('', home, name='index'),

    path('signup/', signup, name='signup'),

    path('signin/', signin, name='signin'),

    path('logout/', logout, name='logout'),

    path('account/', account, name='account'),

    path('deposit/', deposit, name='deposit'),

    path('withdraw/', withdraw, name='withdraw'),

    path('balance/', balance, name='balance'),

    path('loan/', loan, name='loan'),

    path('transaction/', transaction, name='transaction'),

    path('about/', about, name='about'),

    path('contact/', contact, name='contact'),

    path('services/', services, name='services'),       # ✅ add kiya

    path('suggestion/', suggestion, name='suggestion'), # ✅ add kiya

]