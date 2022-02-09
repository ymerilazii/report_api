from django.urls import path
from api.views import error404, get_all_tasks, get_task, get_today, create, update, delete, tasks_report

urlpatterns = [
    path('', get_all_tasks, name='tasks'),
    path('<int:pk>/', get_task, name='tasks_id'),
    path('create', create, name='create'),
    path('<int:pk>/update/', update, name='update'),
    path('<int:pk>/delete/', delete, name='delete'),
    path('today/', get_today, name='today'),
    path('report/<int:year>/<int:month>/<int:day>/', tasks_report, name='tasks_report'),
    path('404/', error404, name='404'),
]
