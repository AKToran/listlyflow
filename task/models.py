from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='name', editable=True, always_update=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(default=1, choices = [(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8')])
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"{self.title} by {self.user}"
