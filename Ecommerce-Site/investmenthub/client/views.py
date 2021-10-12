from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


from .models import Client
from product.forms import ProductForm
from .filters import ProductFilter

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            client = Client.objects.create(name=user.username, created_by=user)


            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'client/register.html', {'form':form})

@login_required
def client_admin(request):
    client = request.user.client
    products = client.products.all()

    myFilter = ProductFilter(request.GET, queryset=products)

    products = myFilter.qs

    return render(request, 'client/client_admin.html', {'products':products, 'myFilter':myFilter})

@login_required
def add_product(request):
    if(request.method == 'POST'):
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.client = request.user.client
            product.slug = slugify(product.title)
            product.save()
            return redirect('client_admin')
    else:
        form = ProductForm()
    return render(request, 'client/add_product.html', {'form':form})
