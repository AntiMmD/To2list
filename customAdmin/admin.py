from django.contrib import admin

from user.models import User
from task.models import Task, Project


class TaskInline(admin.StackedInline):
    model = Task
    extra = 0


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_editable = ['is_staff']
    inlines = [ProjectInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'icon', 'date_created']
    list_filter = ['user']
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'name', 'status', 'priority']
    list_editable = ['priority', 'status']
