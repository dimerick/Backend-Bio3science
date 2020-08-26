from rest_framework import serializers
from django.contrib.auth.models import User



class CustomUserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user