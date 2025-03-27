from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=15, unique=True)



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field='username' ,primary_key=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"Customer: {self.user.username}"


class Company(models.Model):
    class FieldOfWork(models.TextChoices):
        AIR_CONDITIONER = 'Air Conditioner', 'Air Conditioner'
        ALL_IN_ONE = 'All in One', 'All in One'
        CARPENTRY = 'Carpentry', 'Carpentry'
        ELECTRICITY = 'Electricity', 'Electricity'
        GARDENING = 'Gardening', 'Gardening'
        HOME_MACHINES = 'Home Machines', 'Home Machines'
        HOUSE_KEEPING = 'House Keeping', 'House Keeping'
        INTERIOR_DESIGN = 'Interior Design', 'Interior Design'
        LOCKS = 'Locks', 'Locks'
        PAINTING = 'Painting', 'Painting'
        PLUMBING = 'Plumbing', 'Plumbing'
        WATER_HEATERS = 'Water Heaters', 'Water Heaters'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, to_field='username', primary_key=True)
    
    field = models.CharField(
        max_length=70, choices=FieldOfWork.choices, blank=False, null=False)
    
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)

    def __str__(self):
        return f'{self.user.username} ({self.field}) - Rating: {self.rating}'