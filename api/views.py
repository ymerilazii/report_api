from datetime import date

import requests
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.renderers import JSONRenderer

from api.serializers import TaskSerializer
from .models import Task

base_url = 'http://127.0.0.1:8000/'


def error404(request):
    raise NotFound(detail="404 Not Found", code=404)


# Object Initialization
def initialize(pk=None, data=None):
    try:
        if data:
            if pk:
                task = Task.objects.get(pk=pk)
                return TaskSerializer(task, data=data)
            return TaskSerializer(Task, data=data)
        else:
            if pk:
                task = Task.objects.get(pk=pk)
                return TaskSerializer(task)
            tasks = Task.objects.all()
            return TaskSerializer(tasks, many=True)
    except Task.DoesNotExist:
        raise Http404


def get_all_tasks(request):
    tasks = {'tasks': initialize().data}
    return JsonResponse(tasks, status=200)


def get_task(request, pk):
    task = {'task': initialize(pk).data}
    return JsonResponse(task, status=200)


def get_today(request):
    today_obj = Task.objects.filter(created__date=date.today())
    serializer = TaskSerializer(today_obj, many=True)
    today = {'today': serializer.data}
    return JsonResponse(today, status=200)


@csrf_exempt
def create(request):
    data = JSONParser().parse(request)
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'created': serializer.data}, status=201)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def update(request, pk):
    if request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = initialize(pk, data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'updated': serializer.data}, status=204)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def delete(request, pk):
    task = Task.objects.get(pk=pk)
    serializer = TaskSerializer(task)
    response = JsonResponse({'deleted': serializer.data}, status=204)
    task.delete()
    return response


@csrf_exempt
def tasks_report(request, day, month, year):
    dt = date(year, month, day)
    tasks = Task.objects.filter(created__date=dt)
    print(tasks)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse({'tasks': serializer.data}, status=200)


@csrf_exempt
def index(request):
    req = requests.get(url=base_url + 'tasks/today/')
    if request.method == 'POST':
        data = FormParser().parse(request)
        data = JSONRenderer().render(data)
        requests.post(url=base_url + 'tasks/create', data=data)
        messages.success(request, 'Task created successfully')
        return redirect('index')
    return render(request, 'index.html', req.json())


def all_tasks(request):
    r = requests.get(url=base_url + 'tasks/')
    return render(request, 'api.html', r.json())


def today_tasks(request):
    r = requests.get(url=base_url + 'tasks/today/')
    return render(request, 'api.html', r.json())


def report(request):
    if request.method == 'GET':
        year = request.GET['year']
        month = request.GET['month']
        day = request.GET['day']
        r = requests.get(url=f'{base_url}tasks/report/{year}/{month}/{day}/')
        return render(request, 'api.html', r.json())


def delete_task(request, pk):
    requests.delete(url=f'{base_url}tasks/{pk}/delete/')
    messages.success(request, 'Task deleted successfully')
    return redirect('index')
