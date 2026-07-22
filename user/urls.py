from django.urls import path
from .views import *
from task.views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signUp, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('home/', home, name='home'),

    path('project/create/', create_project, name='create_project'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('project/<int:project_id>/edit/', update_project, name='update_project'),
    path('project/<int:project_id>/delete/', delete_project, name='delete_project'),

    path('project/<int:project_id>/add_task/', addTask, name='add_task'),
    path('project/<int:project_id>/delete_task/<int:id>/', deleteTask, name='delete_task'),
    path('project/<int:project_id>/update_task/<int:id>/', updateTask, name='update_task'),
    path('project/<int:project_id>/toggle_task/<int:id>/', toggle_task, name='toggle_task'),
    path('project/<int:project_id>/search/', searchTask, name='search_task'),
]
