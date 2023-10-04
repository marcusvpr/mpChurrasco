from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def logout_view(request):
    """Faz Logout usuário"""
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register_view(request):
    """Faz Registro usuário"""
    if request.method != 'POST':
        """Exibe Form em Branco"""
        form = UserCreationForm()
    else:
        """Processa Form Preenchido"""
        form = UserCreationForm(data = request.POST)
        
        if form.is_valid():
            new_user = form.save()
            """Faz Login e direciona para Home"""
            authenticate_user = authenticate(username = new_user.username,
                                             password = request.POST['password1'])
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('index'))

    context = { 'form': form }
    return render(request, 'mp_users/register.html', context)

