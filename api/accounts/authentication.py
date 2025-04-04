# yourapp/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            return get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            raise AuthenticationFailed('User not found')
