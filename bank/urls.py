from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('about',views.about,name='about'),
    path('services',views.services,name='services'),
    path('suggestion',views.suggestion,name='suggestion'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),      # ← ADD ✅
    path('account/', views.account, name='account'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('balance/', views.balance, name='balance'),
    path('loan/', views.loan, name='loan'),
    path('contact/', views.contact, name='contact'),
    path('transaction/', views.transaction, name='transaction'),  # ← ADD ✅
]
