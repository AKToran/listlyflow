from django import forms
from . import models

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'description', 'due_date', 'priority', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

class TaskFilterForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    priority = forms.ChoiceField(choices = [( '','Priority'), (0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8')], required=False)
    category = forms.ModelChoiceField(queryset=models.Category.objects.all(), empty_label='Category', required=False)