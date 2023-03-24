from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Songs

@receiver(pre_save, sender=Songs)
def update_songs_album(sender, instance, **kwargs):
    if instance.is_single:
        instance.album = None

