from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("AKBANK LIVE 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('bank/', include('bank.urls')),
]