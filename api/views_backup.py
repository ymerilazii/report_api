from datetime import date

from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
import requests

from api.serializers import TaskSerializer
from .models import Task


def error404(request):
    raise NotFound(detail="404 Not Found", code=404)


class TasksAPI(viewsets.ViewSet):
    api_view = ['GET']
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'api.html'

    def __initialize(self, pk=None):
        try:
            if pk:
                task = Task.objects.get(pk=pk)
                return TaskSerializer(task)
            tasks = Task.objects.all()
            return TaskSerializer(tasks, many=True)
        except Task.DoesNotExist:
            error404(self.request)

    def get_all_tasks(self, request):
        tasks = {'tasks': self.__initialize().data}
        return Response(tasks, status=200, template_name=self.template_name)

    def get_task(self, request, pk):
        task = {'task': self.__initialize(pk).data}
        return Response(task, status=200, template_name=self.template_name)

    def get_today(self, request):
        today_obj = Task.objects.filter(created__date=date.today())
        serializer = TaskSerializer(today_obj, many=True)
        today = {'today': serializer.data}
        return Response(today, status=200, template_name=self.template_name)


class TaskCrudAPI(viewsets.ViewSet):
    api_view = ['GET', 'POST', 'PATCH', 'DELETE']
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def __initialize(self, pk=None):
        try:
            if pk:
                task = Task.objects.get(pk=pk)
                return task
        except Task.DoesNotExist:
            error404(self.request)

    def create(self, request):
        serializer = TaskSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk):
        serializer = TaskSerializer(self.__initialize(pk), data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        task = self.__initialize(pk)
        serializer = TaskSerializer(task)
        response = Response(serializer.data, status=204)
        if request.method == 'GET':
            task.delete()
            return redirect('index')
        task.delete()
        return response


def index(request):
    # t = TasksAPI().get_today(request)
    req = requests.get(url='http://127.0.0.1:8000/tasks/today/')
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
        return redirect('index')
    return render(request, 'index.html', req.json())
