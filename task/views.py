from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from . import forms
from . import models

@method_decorator(login_required, name='dispatch')
class AddCategoryView(FormView):
    form_class = forms.CategoryForm
    template_name = 'category.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class AddTaskView(FormView):
    form_class = forms.TaskForm
    template_name = 'task.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        title = form.cleaned_data['title']
        form.save()
        email_subject = "Task Added!"
        email_body = render_to_string('task_added.html', {'user': self.request.user, 'title': title})
        email = EmailMultiAlternatives(email_subject,'', to=[self.request.user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditTaskView(UpdateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'task.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')

def taskdone(request, id):
    task = models.Task.objects.get(id=id)
    task.status = True
    task.priority = 1
    task.save()
    email_subject = "Task Complete!"
    email_body = render_to_string('task_done.html', {'user': request.user, 'task': task})
    email = EmailMultiAlternatives(email_subject,'', to=[request.user.email])
    email.attach_alternative(email_body, "text/html")
    email.send()
    return redirect('home')
    
def deleteTask(request, id):
    task = models.Task.objects.get(id=id)
    task.delete()
    return redirect('home')

