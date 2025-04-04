from django.urls import path
from .views import TaskJobViewSet, TaskViewSet, TaskScheduleViewSet, ScheduleSectionTestViewSet

urlpatterns = [
    path('jobs/', TaskJobViewSet.as_view({'get': 'list', 'post' : 'create'})),
    path('', TaskViewSet.as_view({'get': 'list'})),
    path('<int:pk>/roadmap/', TaskViewSet.as_view({'get' : 'roadmap'})),
    path('<int:pk>/', TaskViewSet.as_view({'get' : 'retrieve'})),
    path('progress/', TaskViewSet.as_view({'get': 'progress'})),
    path('schedules/today/', TaskScheduleViewSet.as_view({'get': 'get_today_schedules'})),
    path('schedules/<int:pk>/', TaskScheduleViewSet.as_view({'get': 'retrieve'})),
    path('schedules/<int:pk>/<int:index>/chat/', TaskScheduleViewSet.as_view({'post': 'chat'})),
    path('schedules/<int:pk>/status/', TaskScheduleViewSet.as_view({'get': 'status_toggle'})),
    path('schedules/', TaskScheduleViewSet.as_view({'get': 'list'})),
     path('schedules/<int:id>/test/<int:index>/<int:type>/', TaskScheduleViewSet.as_view({'get': 'test'})),
     path('schedules/<int:id>/test/eval/<int:index>/<str:type>/<int:pk>/', ScheduleSectionTestViewSet.as_view({'get': 'eval'})),
     path('schedules/<int:id>/test/fetch/<str:type>/<int:index>/', ScheduleSectionTestViewSet.as_view({'get': 'fetch_tests'})),
     path('schedules/test/save/', ScheduleSectionTestViewSet.as_view({'post': 'save'})),
     path('schedules/test/<int:pk>/', ScheduleSectionTestViewSet.as_view({'delete': 'destroy'})),
    path('schedules/calendar/<int:task>/<int:year>/<int:month>/', TaskScheduleViewSet.as_view({'get': 'schedules_calendar'})),
]
