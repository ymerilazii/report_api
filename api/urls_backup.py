from django.urls import path
from api.views import TasksAPI, error404, TaskCrudAPI

urlpatterns = [
    path('', TasksAPI.as_view({'get': 'get_all_tasks'}), name='tasks'),
    path('<int:pk>/', TasksAPI.as_view({'get': 'get_task'}), name='tasks_id'),
    path('create', TaskCrudAPI.as_view({'post': 'create'}), name='create'),
    path('<int:pk>/update/', TaskCrudAPI.as_view({'patch': 'update'}), name='update'),
    path('<int:pk>/delete/', TaskCrudAPI.as_view({'delete': 'delete', 'get': 'delete'}), name='delete'),
    path('today/', TasksAPI.as_view({'get': 'get_today'}), name='today'),
    path('404/', error404, name='404'),
]
