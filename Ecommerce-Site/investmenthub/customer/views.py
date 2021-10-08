from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Customer
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            customer = Customer.objects.create(name=user.username, created_by=user)


            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'customer/register.html', {'form':form})