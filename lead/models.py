from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)  

class Profile(models.Model):
    GenderChoice = (('Male','Male'), ('Female','Female'),('Others','Others'))
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, choices=GenderChoice)
    contact = models.CharField(validators = [phoneNumberRegex], max_length = 16)
    avatar = models.ImageField(upload_to='profile_pics', default='default.png')
    signup_confirmation = models.BooleanField(default=False)

    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/media/default.png"

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        image = Image.open(self.avatar.path)
        if image.height > 300 or image.width > 300:
            image.thumbnail((150,150))
            image.save(self.avatar.path)

class Lead(models.Model):
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    email = models.EmailField()
    description = models.TextField(max_length=255)
    contact = models.CharField(validators = [phoneNumberRegex], max_length = 16)
    date_created = models.DateField(auto_now_add=True)
    agent = models.ForeignKey('Agent', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey('Profile', on_delete=models.CASCADE)    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['-id']

class Agent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    organisation = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email}'
    
    class Meta:
        ordering = ['-date_created']
    
class Category(models.Model):
    CATAGORY_CHOICES = (('Contacted', 'Contacted'), ('Unassigned', 'Unassigned'), ('Converted', 'Converted'))
    name = models.CharField(max_length=200, choices=CATAGORY_CHOICES)
    organisation = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'