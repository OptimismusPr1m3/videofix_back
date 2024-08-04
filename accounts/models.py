from django.db import models
from authemail.models import EmailUserManager, EmailAbstractUser

# Create your models here.


class MyUser(EmailAbstractUser):
    date_of_birth = models.DateField('Date of birth', null=True, blank=True)

    objects = EmailUserManager()
    
    
class VerifiedUserManager(EmailUserManager):
    def get_queryset(self):
        return super(VerifiedUserManager, self).get_queryset().filter(
            is_verified=True)


class VerifiedUser(MyUser):
    objects = VerifiedUserManager()

    class Meta:
        proxy = True