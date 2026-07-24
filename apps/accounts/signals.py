from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, User

@receiver(post_save,sender=User)
def ensure_profile(sender,instance,created,**kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
