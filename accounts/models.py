from django.db import models
from authemail.models import EmailUserManager, EmailAbstractUser

# Create your models here.


class MyUser(EmailAbstractUser):
    date_of_birth = models.DateField('Date of birth', null=True, blank=True)
    street = models.CharField('Street', null=True, blank=True, max_length=20)
    street_number = models.IntegerField('Streetnumber', null=True, blank=True)
    zip_code = models.CharField('Zip Code', null=True, blank=True, max_length=20)
    city = models.CharField('City', null=True, blank=True, max_length=20)
    country = models.CharField('Country', null=True, blank=True, max_length=20)
    phone_number = models.CharField('Phonenumber', null=True, blank=True, max_length=20)
    my_videos = models.JSONField(blank=True, null=True)
    video_timestamps = models.JSONField(blank=True, null=True)
    objects = EmailUserManager()
    
    
class VerifiedUserManager(EmailUserManager):
    def get_queryset(self):
        return super(VerifiedUserManager, self).get_queryset().filter(
            is_verified=True)


class VerifiedUser(MyUser):
    objects = VerifiedUserManager()

    class Meta:
        proxy = True
