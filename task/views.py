from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from task.form import CreateTask, ProjectForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import re


def _sort_tasks(tasks):
    iu, u, i, c = [], [], [], []
    for task in tasks:
        if task.priority == 'IU':
            iu.append(task)
        elif task.priority == 'U':
            u.append(task)
        elif task.priority == 'I':
            i.append(task)
        else:
            c.append(task)
    return iu + u + i + c


def _user_project(request, project_id):
    return get_object_or_404(request.user.projects, id=project_id)


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def home(request):
    projects = request.user.projects.all()
    return render(request, 'home.html', {
        'projects': projects,
        'active_project': None,
    })


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def project_detail(request, project_id):
    project = _user_project(request, project_id)
    tasks = _sort_tasks(project.tasks.all())
    projects = request.user.projects.all()
    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks,
        'projects': projects,
        'active_project': project,
    })


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def create_project(request):
    projects = request.user.projects.all()
    if request.method == 'GET':
        form = ProjectForm()
        return render(request, 'createProject.html', {
            'form': form,
            'projects': projects,
            'active_project': None,
        })

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect(reverse('project_detail', args=[project.id]))
        return render(request, 'createProject.html', {
            'form': form,
            'projects': projects,
            'active_project': None,
        })

    return HttpResponse('only get and post method are allowed')


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def update_project(request, project_id):
    project = _user_project(request, project_id)
    projects = request.user.projects.all()

    if request.method == 'GET':
        form = ProjectForm(instance=project)
        return render(request, 'updateProject.html', {
            'form': form,
            'project': project,
            'projects': projects,
            'active_project': project,
        })

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(reverse('project_detail', args=[project.id]))
        return render(request, 'updateProject.html', {
            'form': form,
            'project': project,
            'projects': projects,
            'active_project': project,
        })

    return HttpResponse('only get and post method are allowed')


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def delete_project(request, project_id):
    if request.method == 'POST':
        project = _user_project(request, project_id)
        project.delete()
    return redirect(reverse('home'))


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def addTask(request, project_id):
    project = _user_project(request, project_id)
    projects = request.user.projects.all()

    if request.method == 'GET':
        form = CreateTask()
        return render(request, 'createTask.html', {
            'form': form,
            'project': project,
            'projects': projects,
            'active_project': project,
        })

    if request.method == 'POST':
        form = CreateTask(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.project = project
            task.save()
            project.save()  # bump updated_at
            return redirect(reverse('project_detail', args=[project.id]))
        return render(request, 'createTask.html', {
            'form': form,
            'project': project,
            'projects': projects,
            'active_project': project,
        })

    return HttpResponse('only get and post method are allowed')


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def deleteTask(request, project_id, id):
    project = _user_project(request, project_id)
    if request.method == 'POST':
        task = get_object_or_404(project.tasks, id=id, user=request.user)
        task.delete()
        project.save()
    return redirect(reverse('project_detail', args=[project.id]))


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def updateTask(request, project_id, id):
    project = _user_project(request, project_id)
    task = get_object_or_404(project.tasks, id=id, user=request.user)
    projects = request.user.projects.all()

    if request.method == 'GET':
        form = CreateTask(instance=task)
        return render(request, 'updateTask.html', {
            'form': form,
            'project': project,
            'projects': projects,
            'active_project': project,
        })

    if request.method == 'POST':
        form = CreateTask(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.project = project
            task.save()
            project.save()
            return redirect(reverse('project_detail', args=[project.id]))
        return render(request, 'updateTask.html', {
            'form': form,
            'project': project,
            'projects': projects,
            'active_project': project,
        })

    return HttpResponse('only get and post method is allowed')


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def toggle_task(request, project_id, id):
    project = _user_project(request, project_id)
    if request.method == 'POST':
        task = get_object_or_404(project.tasks, id=id, user=request.user)
        task.status = 'D' if task.status == 'P' else 'P'
        task.save()
        project.save()
    return redirect(reverse('project_detail', args=[project.id]))


@login_required(login_url=reverse_lazy('login'))
def searchTask(request, project_id):
    project = _user_project(request, project_id)
    projects = request.user.projects.all()
    error = ''
    task_name = request.GET.get('task_name', '')

    if task_name:
        safe_task_name = re.escape(task_name)
        tasks = project.tasks.filter(name__regex=rf'.*{safe_task_name}.*')
        if tasks.count() == 0:
            tasks = project.tasks.all()
            error = 'No tasks matched your search.'
    else:
        tasks = project.tasks.all()

    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': _sort_tasks(tasks),
        'projects': projects,
        'active_project': project,
        'error': error,
        'search_query': task_name,
    })
