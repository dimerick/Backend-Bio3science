from rest_framework import serializers
from .models import CustomUser, Profile, Degree, FieldsOfStudy



class CustomUserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Profile
        fields = '__all__'
        
    def create(self, validated_data):
        obj = super(ProfileSerializer, self).create(validated_data)
        obj.save()
        return obj

class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = '__all__'

class FieldsOfStudySerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldsOfStudy
        fields = '__all__'