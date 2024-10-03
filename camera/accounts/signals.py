from django.db.models.signals import post_save  # add this
from .models import User, Profile
from django.dispatch import receiver


@receiver(post_save, sender=User)  # add this
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)  # add this
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
