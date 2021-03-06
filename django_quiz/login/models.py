from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


def upload_to(instance, filename):
    return 'user_profile_image/{}/{}'.format(instance.user_id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(max_length=500,blank=True)
    total_score = models.IntegerField(blank=True,null=True)
    favourite_categories = models.ManyToManyField('qna.Category',blank=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to=upload_to)

    def __str__(self):
        return "%s %s" %(self.id,self.user)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)

