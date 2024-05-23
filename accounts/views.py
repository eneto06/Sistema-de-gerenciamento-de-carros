from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def register_view(request):
    #O if roda quando o usuário preenche os dados de login
    if request.method == 'POST':
        #Valida os dados do usuário    
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            #Redireciona para a tela de login
            return redirect('login')
    else:
        #Cria um formulário vazio para o nosso usuário
        user_form = UserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})

def login_view(request):
    if request.method == 'POST':
        #Capturando duas variáveis
        username = request.POST["username"]
        password = request.POST["password"]
        #Faz a autenticação do login do usuário
        user = authenticate(request, username = username, password = password)
        #Se o usuário existe
        if user is not None:
            #Faça login 
            login(request, user)
            return redirect('cars_list')
        else:
            login_form = AuthenticationForm()
    else:
        #Renderiza o nosso form de login vazio
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    return redirect('cars_list')