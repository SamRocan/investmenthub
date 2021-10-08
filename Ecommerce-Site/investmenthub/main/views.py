from django.shortcuts import render

# Create your views here.s
def homepage(request):
    return render(request, 'main/homepage.html')