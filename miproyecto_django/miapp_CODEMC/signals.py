from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser, BusinessManager, Empleado

@receiver(post_save, sender=CustomUser)
def asignar_grupo(sender, instance, created, **kwargs):
    print("Señal ejecutada para:", instance.username) 
    print(instance.groups)
    print(created)
    if created:
        if instance.is_superuser:
            group, created = Group.objects.get_or_create(name='Managers')
            instance.groups.add(group)

            BusinessManager.objects.get_or_create(user=instance)

        elif instance.rol == CustomUser.MANAGER:
            group, created = Group.objects.get_or_create(name='Managers')
            instance.groups.add(group)
        else:
            group, created = Group.objects.get_or_create(name='Empleados')
            instance.groups.add(group)
    print(instance.groups)