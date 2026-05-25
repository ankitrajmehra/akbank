from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('balance/', views.balance, name='balance'),
    path('loan/', views.loan, name='loan'),
    path('transaction/', views.transaction, name='transaction'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('suggestion/', views.suggestion, name='suggestion'),
]