from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer, RegisterSerializer
from .models import User



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def partial_update(self, request, pk):
        user = request.user

        print(request.data)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        user = request.user
        profileImage = "https://www.strasys.uk/wp-content/uploads/2022/02/Depositphotos_484354208_S.jpg"
        try:
            if(user.profile):
                profileImage = f"http://localhost:8000{user.profile.url}"
        except:
            pass
        return Response({'email' : user.email, 'full_name' : user.full_name, 'profile' : profileImage})
    
    def profile(self, request):
        user = request.user
        profileImage = "https://www.strasys.uk/wp-content/uploads/2022/02/Depositphotos_484354208_S.jpg"
        try:
            if(user.profile):
                profileImage = f"http://localhost:8000{user.profile.url}"
        except:
            pass
        return Response({'email' : user.email, 'full_name' : user.full_name, 'country' : user.country, 'timezone' : user.timezone,  'profile' : profileImage})


    

    





class GetUserFirstNameView(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        return Response({'firstname': request.user.email})


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def today(self, request):
        print(request.user.id)
        return Response(self.serializer_class(Notification.objects.filter(account = request.user), many=True).data)
