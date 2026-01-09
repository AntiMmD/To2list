from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from user.form import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import re

@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def home(request):
    if request.method=='GET':
        allTasks = request.user.tasks.all()
        sortedTasks= []
        iuTasks= []
        uTasks= []
        iTasks= []
        cTasks= []
        for task in allTasks:
            if task.priority == 'IU':
                iuTasks.append(task)

            elif task.priority == 'U':
                uTasks.append(task)
            
            elif task.priority == 'I':
                iTasks.append(task)

            elif task.priority == 'C':
                cTasks.append(task)


        sortedTasks+= iuTasks + uTasks + iTasks + cTasks

        return render(request ,'home.html', {'tasks': sortedTasks}) 


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def addTask(request):

    if request.method == 'GET':
        form = CreateTask()
        return render(request, 'createTask.html', {'form': form})
    
    elif request.method == 'POST':
        form = CreateTask(request.POST)

        if form.is_valid():
            request.user.tasks.create(**form.cleaned_data , user = request.user)
        return redirect(reverse('home'))
    
    else:
        HttpResponse("only get and post method are allowed")


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def deleteTask(request, id):

    if request.method == 'POST':    
        request.user.tasks.get(id=id).delete()
    
    return redirect(reverse('home'))


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def updateTask(request,id):

    task = request.user.tasks.get(id=id)
    if request.method == 'GET':
        form = CreateTask(instance = task)
        return render(request, 'updateTask.html', {'form': form})
    
    if request.method == 'POST':
        form = CreateTask(request.POST, instance = task )

        if form.is_valid():
            task= form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(reverse('home'))
        else:
            return redirect(reverse('home'))

    else:
        HttpResponse("only get and post method is allowed")

    
def searchTask(request):
    error = ''
    task_name = request.GET.get('task_name', '')
    
    if task_name:
        print(task_name)
        safe_task_name = re.escape(task_name)
        tasks = request.user.tasks.filter(name__regex =rf".*{safe_task_name}.*")
        if tasks.count()==0:
            tasks = request.user.tasks.all()
            error = 'no item mathced!'  
        
    else:
        tasks = request.user.tasks.all()  

    return render(request, 'home.html', {'tasks': tasks, 'error':error})