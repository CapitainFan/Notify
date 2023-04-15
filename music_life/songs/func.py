from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Songs


@receiver(pre_save, sender=Songs)
def update_songs_album(sender, instance, **kwargs):
    '''
    Запрещает одновременныый выбор
    поля is_single и поля album
    в таблице Songs
    '''
    if instance.is_single:
        instance.album = None
