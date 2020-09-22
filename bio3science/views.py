from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.http import Http404
import googlemaps
from django.conf import settings

# Create your views here.

class HelloBio3science(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


    def get(self, request):
        content = {"message": "Alersnet Rocking"}
        return Response(content)

class Place(APIView):
    #permission_classes = [permissions.IsAuthenticated]


    def get(self, request, input_search):

        gmaps = googlemaps.Client(key=settings.GOOGLE_KEY)

        #input_search = request.get['input_search']

        result = gmaps.find_place(input_search, 'textquery', ['business_status', 'formatted_address', 'geometry', 'icon', 'name', 'photos', 'place_id', 'plus_code', 'types'])

        return Response(result)

class AccountList(APIView):

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class AccountDetail(APIView):

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print(pk)
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

