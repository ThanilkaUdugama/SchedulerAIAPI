from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Notification

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    profile = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'country', 'timezone', 'password', 'confirm_password', 'profile')

    def validate(self, attrs):
        if('password' in attrs):
            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            country=validated_data['country'],
            timezone=validated_data['timezone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.country = validated_data.get('country', instance.country)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.profile = validated_data.get('profile', instance.profile)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
    



class NotificationSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'


