from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["email"]


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth = models.DateField(null=True, blank=True)  # Add birth field

    def __str__(self):
        return f"Customer: {self.user.username}"


class Company(models.Model):
    FIELD_CHOICES = [
        ('Air Conditioner', 'Air Conditioner'),
        ('All in One', 'All in One'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    field = models.CharField(max_length=70, choices=FIELD_CHOICES)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

    def __str__(self):
        return f"Company: {self.user.username} ({self.field})"
