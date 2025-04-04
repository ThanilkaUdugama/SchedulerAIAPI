from django.db import models
from accounts.models import User

# Resources : https://www.youtube.com/watch?v=5DW4Ky1Um4o
# Refer : Python Django Models

# Malintha
class TaskJob(models.Model):
    pass # remove this line after writing the code.
    #define object properties defined below

    # account: Link to the User model (Account) for the task owner.
    # Use this to associate each task with a specific user.

    # prompt: A text field to store the task description or prompt.
    # This is where the task details should be stored.

    # start_date: A date field representing the start date of the task.
    # The developer should enter the task's start date here.

    # end_date: A date field representing the end date of the task.
    # The developer should enter the task's completion date here.

    # theme_color: A string field to store the theme color for the task.
    # This could be used for UI purposes (e.g., a color code or name).

    # allocated_time: A JSON field to store time-related data.
    # This can hold various time-related values (e.g., start time, end time).

    # generated: A boolean field to track if the task has been generated or processed.
    # Set to True once the task has been completed or generated, otherwise False.

# Chamod
class Task(models.Model):
    pass # remove this line after writing the code.
    #define object properties defined below
    # icon: A string field to store the icon associated with the task.
    # This could be a URL, icon name, or class reference for the task icon.

    # title: A string field to store the title of the task.
    # This is the name or heading that will represent the task.

    # taskjob: A ForeignKey field linking the Task to a specific TaskJob.
    # This establishes the relationship between a task and the task it is associated with.

    # created_at: A date-time field that automatically records the time when the task was created.
    # This field is auto-populated when a new task is created.

    # updated_at: A date-time field that automatically records the last time the task was updated.
    # This field is automatically updated whenever the task is modified.

# Malintha
class TaskSchedule(models.Model):
    STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('incomplete', 'Incomplete'),
        ('remaining', 'Remaining'),
    ]
    #define object properties defined below

    # STATUS_CHOICES (given): A list of choices for the status field.
    # Define the possible statuses a task schedule can have: 'Complete', 'Incomplete', 'Remaining'.
    # This will be used to track the current state of the task schedule.

    # task: A ForeignKey field linking the TaskSchedule to a specific Task.
    # This establishes the relationship between a task schedule and the task it belongs to.

    # heading: A string field to store the heading or title of the task schedule.
    # This should describe the specific schedule or task being tracked.

    # icon: A string field to store the icon related to the task schedule.
    # This could be an icon name, URL, or class reference for visual representation.

    # status: A string field to represent the current status of the task schedule.
    # Use the STATUS_CHOICES to restrict values to 'complete', 'incomplete', or 'remaining'.
    # This field helps in tracking the progress of the task schedule.

    # content: A JSON field to store additional data for the task schedule.
    # This could include detailed content or metadata related to the schedule (e.g., notes, attachments, etc.).

    # date: A date field to store the scheduled date for the task.
    # This is the specific date when the task schedule is to be completed or reviewed.

    # startTime: A time field to store the start time of the task schedule.
    # This marks the start time for the scheduled task.

    # endTime: A time field to store the end time of the task schedule.
    # This marks the end time for the scheduled task.

    # content_generated: A boolean field to track if the task schedule's content has been generated.
    # Set to True once the content for the schedule is generated, otherwise False.

# Thanilka
class ScheduleSectionTest(models.Model):
    MCQ = 'mcq'
    ESSAY = 'essay'
    CODE = 'code'
    
    QUESTION_TYPE_CHOICES = [
        (MCQ, 'Multiple Choice'),
        (ESSAY, 'Essay'),
        (CODE, 'Code'),
    ]

    schedule = models.ForeignKey(TaskSchedule, on_delete=models.CASCADE, related_name='section_tests')
    sectionIndex = models.IntegerField()
    questions = models.JSONField() 
    answers = models.JSONField()   
    marks = models.IntegerField() 
    type = models.CharField(
            max_length=10,
            choices=QUESTION_TYPE_CHOICES,
            default=MCQ
        )


    def __str__(self):
        return f"ScheduleSectionTest {self.id} for Schedule {self.schedule.name}, Section {self.sectionIndex}"