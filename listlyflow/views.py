from django.shortcuts import render, redirect
from task.models import Task, Category

def home(request, slug = None):
    search = request.GET.get('search')
    if request.user.is_authenticated:
        user = request.user
        if slug is not None:
            category = Category.objects.get(slug=slug)
            data = Task.objects.filter(category=category, user=user).order_by('status')

        elif search:
            data = Task.objects.filter(user=user, title__icontains=search)
            if len(data) < 1:
                data = Task.objects.filter(user=user, category__name__icontains=search)

                if len(data) < 1:
                    data = Task.objects.filter(user=user, priority__icontains=search)

                    if len(data) < 1:
                        data = Task.objects.filter(user=user, due_date__icontains=search)


        
        else:
            data = Task.objects.filter(user=user).order_by('status')
    else :     
        data = {}
    categories = Category.objects.all()
    return render(request, 'home.html', {'data': data,'categories': categories})

def sortByPriority(request, bool):
    if request.user.is_authenticated:
        user = request.user
        if bool.lower() == 'true':
            data = Task.objects.filter(user=user).order_by('status','-priority')
        else:
            data = Task.objects.filter(user=user).order_by('status','priority')
    else:
        data = {}
    categories = Category.objects.all()
    return render(request, 'home.html', {'data': data,'categories': categories})

