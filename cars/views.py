
from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator    
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

   


class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains = search)
        return cars
    
    
class NewCarsView(View):
    def get(self, request):
        # Condição é atendida quando o usuário cadastra um carro novo
        if request.method == 'POST':
            # request.POST: pega as informações do POST que o usuário faz
            # request.FILES: Pega os Arquivos que o usuário envia no metodo POST
            new_car_form = CarModelForm(request.POST, request.FILES)
            #Verifica se os dados do formulário estão válidos
            if new_car_form.is_valid():
                #Salva no banco de dados o carro cadastrado pelo usuário
                new_car_form.save()
                #Redireciona o usuário para a lista de carros
                return redirect('cars_list')
    def post(self, request):
        new_car_form = CarModelForm()
        return render(request, 'new_car.html', {'new_car_form': new_car_form})

@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
    
    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs = {'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'