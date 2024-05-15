from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm

# O usuário acessou o '/cars/' e ativou essa função 
def cars_view(request):

    # Essa variável percorre todo os objetos do model 'Car' (<Query set>)
    cars = Car.objects.all().order_by('model')

    # Variável que contém a busca feita pelo usuário 
    search = request.GET.get('search')

    ''' Condição que verifica se a busca é nula,
        se não for filter(model__contais = search)
        busca a pesquisa feita pelo usuário
    '''    
    if search:
        cars = Car.objects.filter(model__contains=search)

    return render(
        request, 
        'cars.html', 
        {'cars': cars} 
        )

def new_car_view(request):

    # Condição é atendida quando o usuário cadastra um carro novo
    if request.method == 'POST':
        # request.POST: pega as informações do POST que o usuário faz
        # request.FILES: Pega os Arquivos que o usuário envia no metodo POST
        new_car_form = CarModelForm(request.POST, request.FILES)
        #Verifica se os dados do formulário estão válidos
        if new_car_form.is_valid():
            #Salva no banco de dados o nosso carro cadastrado
            new_car_form.save()
            #Redireciona o usuário para a lista de carros
            return redirect('cars_list')
    else:
        new_car_form = CarModelForm()
        return render(request, 'new_car.html', {'new_car_form': new_car_form})