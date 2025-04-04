from django.urls import path
from .views import RegisterView, GetUserFirstNameView, NotificationViewSet, AccountViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change/<int:pk>/', AccountViewSet.as_view({'patch': 'partial_update'})),
    path('<int:pk>/', AccountViewSet.as_view({'get': 'retrieve'})),
    path('notifications/', NotificationViewSet.as_view({'get': 'today'}), name='notifications'),
    path('notifications/today/', NotificationViewSet.as_view({'get': 'today'})),
    path('profile/', AccountViewSet.as_view({'get' : 'profile'})), 
]
