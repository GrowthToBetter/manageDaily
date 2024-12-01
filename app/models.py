from datetime import timezone, datetime
from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
# Create your models here.

from django.db import models

# Models
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.session_key}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('TRANSPORT', 'Transport'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('OTHERS', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.now)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"


