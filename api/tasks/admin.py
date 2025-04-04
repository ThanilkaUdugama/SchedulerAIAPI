from django.contrib import admin
from .models import TaskJob, Task, TaskSchedule

admin.site.register(TaskJob)
admin.site.register(Task)
admin.site.register(TaskSchedule)