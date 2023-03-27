from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AdditionalLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.link


class Hobby(models.Model):
    hobby = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.hobby

class SocialMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.hobby

class Skills(models.Model):
    category = models.CharField(max_length=255)
    skill = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.category}: {self.skill}"

class UserData(models.Model):
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(auto_now_add=True)
    hobbies = models.ManyToManyField(Hobby)
    profile_views = models.IntegerField(default=0)
    photo = models.ImageField(blank=True, null=True)
    role = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=2555)
    skills = models.ManyToManyField(Skills)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
class Employment(models.Model):
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period_from = models.DateField()
    period_through = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title