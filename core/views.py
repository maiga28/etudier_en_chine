from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
def universities(request):
    """Page des universités"""
    return render(request, 'universities/universities.html')

def bourses(request):
    """Page des bourses"""
    return render(request, 'bourses/bourses.html')

def services(request):
    """Page des services"""
    return render(request, 'services/services.html')

def about(request):
    """Page à propos"""
    return render(request, 'about/about.html')

def contact(request):
    """Page de contact"""
    return render(request, 'contact/contact.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# ... vos autres vues ...

def login_view(request):
    """Page de connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Identifiants invalides')
    return render(request, 'auth/login.html')

def register_view(request):
    """Page d'inscription"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compte créé avec succès !')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})