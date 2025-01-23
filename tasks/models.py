from django.db import models
from django.conf import settings


class Task(models.Model):
    STATUS_CHOICES = [
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=225, null=False)
    description = models.CharField(max_length=128, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Incomplete")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name