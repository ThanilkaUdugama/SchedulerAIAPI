from rest_framework import serializers
from .models import TaskJob, Task, TaskSchedule, ScheduleSectionTest

class TaskJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskJob
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskScheduleSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), source='task', write_only=True
    )  # Allow setting task by ID

    class Meta:
        model = TaskSchedule
        fields = '__all__'

class ScheduleSectionTestSerializer(serializers.ModelSerializer):
    schedule = serializers.PrimaryKeyRelatedField(queryset=TaskSchedule.objects.all()) 
    
    class Meta:
        model = ScheduleSectionTest
        fields = ['id', 'schedule', 'sectionIndex', 'questions', 'answers', 'marks', 'type']