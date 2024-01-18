from django.shortcuts import render, redirect
from task.models import Task, Category
from django.contrib.auth.decorators import login_required
from task.forms import TaskFilterForm

def home(request, slug = None):
    form = TaskFilterForm()
    search = request.GET.get('search')
    if request.user.is_authenticated:
        user = request.user
        if slug is not None:
            category = Category.objects.get(slug=slug)
            data = Task.objects.filter(category=category, user=user).order_by('status')

        elif search:
            data = Task.objects.filter(user=user, title__icontains=search).order_by('status')
            if len(data) < 1:
                data = Task.objects.filter(user=user, category__name__icontains=search).order_by('status')

                if len(data) < 1:
                    data = Task.objects.filter(user=user, priority__icontains=search).order_by('status')

                    if len(data) < 1:
                        data = Task.objects.filter(user=user, due_date__icontains=search).order_by('status')
        
        else:
            data = Task.objects.filter(user=user).order_by('status')
    else :     
        data = {}
    categories = Category.objects.all()
    return render(request, 'home.html', {'data': data,'categories': categories, 'form': form})

@login_required
def sortByPriority(request, bool):
    user = request.user
    form = TaskFilterForm()
    if bool.lower() == 'true':
        data = Task.objects.filter(user=user).order_by('status','-priority')
    else:
        data = Task.objects.filter(user=user).order_by('status','priority')
   
    categories = Category.objects.all()
    return render(request, 'home.html', {'data': data,'categories': categories, 'form': form})

@login_required
def sortByDate(request, bool):
    user = request.user
    form = TaskFilterForm()
    if bool.lower() == 'true':
        data = Task.objects.filter(user=user).order_by('due_date')
    else:
        data = Task.objects.filter(user=user).order_by('-due_date')
   
    categories = Category.objects.all()
    return render(request, 'home.html', {'data': data,'categories': categories, 'form': form})

@login_required
def findSpecificTask(request):
    user = request.user
    form = TaskFilterForm()
    date = request.GET.get('date', None)
    priority = request.GET.get('priority')
    category = request.GET.get('category')
    data = Task.objects.filter(user=user).order_by('status')
       
    if date:
        data = data.filter(due_date=date)
    if priority:
        data = data.filter(priority=priority)
    if category:
        data = data.filter(category=category)

    categories =Category.objects.all()
    return render(request, 'home.html', {'data': data,'categories': categories, 'form': form})


