import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm

logger = logging.getLogger(__name__)

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            logger.info(f"Tarea creada por {request.user}: '{task.content}' (ID: {task.id})")
            return redirect('tasks:task-list')
        else:
            logger.warning(f"Formulario inválido al crear tarea por {request.user}: {form.errors}")
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.is_completed = not task.is_completed
        task.save()
        logger.info(f"Usuario {request.user} cambió estado de tarea (ID: {task.id}) a {'completada' if task.is_completed else 'pendiente'}.")
    return redirect('tasks:task-list')

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        logger.info(f"Usuario {request.user} eliminó la tarea (ID: {task.id}, contenido: '{task.content}').")
        task.delete()
    return redirect('tasks:task-list')