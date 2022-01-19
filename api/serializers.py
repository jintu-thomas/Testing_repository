from rest_framework import serializers
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile



# User = get_user_model()

class UserRegister(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields=['username','password','email','password2']
        
    def save(self):
        reg = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'password doesnt match'})
        reg.set_password(password)
        reg.save()
        return reg

#--------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------


class UpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField()
    location = serializers.CharField()
    birth_date= serializers.DateField()

    class Meta:
        model = Profile
        fields=['bio','location','birth_date']


    def save_fields(self,user):
        user.profile.bio = self.validated_data['bio']
        user.profile.location = self.validated_data['location']
        user.profile.birth_date = self.validated_data['birth_date']
        user.save()
        return user