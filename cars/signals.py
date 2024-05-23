
from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from cars.models import Car, CarInventory


def car_inventory_update():
    #Calcula a quantidade carros que tem no estoque
    cars_count = Car.objects.all().count()
    #Calcula o valor da soma dos carros que tem no estoque
    cars_value = Car.objects.aggregate(
        total_value = Sum('value')
    )['total_value']
    #Cria um registro do inventório de carros
    CarInventory.objects.create(
        cars_count = cars_count,
        cars_value = cars_value
    )


#Receiver recebe o signal
@receiver(post_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    car_inventory_update()

@receiver(post_delete, sender=Car)
def car_pre_save(sender, instance, **kwargs):
     car_inventory_update()

   