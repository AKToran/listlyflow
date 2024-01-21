from django.db import models

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
         return f"{self.name} on {self.date}"

    class Meta:
         verbose_name_plural = 'Contact Us'