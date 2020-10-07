from rest_framework import serializers
from .models import CustomUser, Profile, University, Degree, FieldsOfStudy, Project, Community, ProjectXUniversity, ProjectXCommunity



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

class UniversitySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = University
        fields = '__all__'
        
    def create(self, validated_data):
        obj = super(UniversitySerializer, self).create(validated_data)
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

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = '__all__'

class ProjectXUniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectXUniversity
        fields = '__all__'

class ProjectXCommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectXCommunity
        fields = '__all__'