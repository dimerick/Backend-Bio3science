from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser, Profile, University, Degree, FieldsOfStudy, Project, Community, ProjectXUniversity, ProjectXCommunity, ProjectXUser
from .serializers import CustomUserSerializer, ProfileSerializer, UniversitySerializer, DegreeSerializer, ProjectSerializer, CommunitySerializer, ProjectXUniversitySerializer, ProjectXCommunitySerializer, ProjectXUserSerializer
from django.http import Http404
import googlemaps
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone

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

        #result = gmaps.find_place(input_search, 'textquery', ['business_status', 'formatted_address', 'geometry', 'icon', 'name', 'photos', 'place_id', 'plus_code', 'types'])

        result = gmaps.places_autocomplete_query(input_search, 3)

        return Response(result)

class AccountList(APIView):

    def get(self, request, format=None):

        email = request.GET.get('email', None)
        if(email):
            objs = CustomUser.objects.filter(email=email)
        else:
            objs = CustomUser.objects.all()
            
        serializer = CustomUserSerializer(objs, many=True)
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
    
    def get(self, request, pk=None, format=None):

        
        obj = self.get_object(pk)
        
        serializer = CustomUserSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = CustomUserSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class AccountByEmail(APIView):
        
#     def get(self, request, email, format=None):
#         user = get_object_by_email(email)
#         serializer = CustomUserSerializer(user)
#         return Response(serializer.data)

class ProfileList(APIView):

    def get(self, request, format=None):
        objs = Profile.objects.all()
        serializer = ProfileSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            obj = serializer.save()
            if obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UniversityList(APIView):

    def get(self, request, format=None):

        name = request.GET.get('name', None)
        if(name):
            objs = University.objects.filter(name__icontains=name)
        else:
            objs = University.objects.all()

        serializer = UniversitySerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UniversitySerializer(data=request.data)
        
        if serializer.is_valid():
            obj = serializer.save()
            if obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UniversityDetail(APIView):    

    def get_object(self, pk):
        try:
            return University.objects.get(id=pk)
        except University.DoesNotExist:
            raise Http404

    
    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = UniversitySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)

        # created_by = request.GET.get('created_by', None)
        # if(created_by):
        #     obj.created_by = CustomUser.objects.get(id=created_by)
        #     obj.save()
        #     serializer = UniversitySerializer(data=obj)
        #     if serializer.is_valid():
        #         return Response(serializer.data)

        serializer = UniversitySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DegreeList(APIView):

    def get(self, request, format=None):
        degrees = Degree.objects.all()
        serializer = DegreeSerializer(degrees, many=True)
        return Response(serializer.data)

class FieldsOfStudyList(APIView):

    def get(self, request, format=None):
        items = FieldsOfStudy.objects.all()
        serializer = DegreeSerializer(items, many=True)
        return Response(serializer.data)

class GenerateTokenResetPassword(APIView):

    def get_object(self, email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request):
        email = request.GET.get('email', None)
        obj = self.get_object(email)
        token = default_token_generator.make_token(obj)
        print(token)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        user.last_login = timezone.now()
        user.save()
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ProjectList(APIView):

    def get(self, request, format=None):

        name = request.GET.get('name', None)
        if(name):
            objs = Project.objects.filter(name__icontains=name)
        else:
            objs = Project.objects.all()

        serializer = ProjectSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        
        if serializer.is_valid():
            obj = serializer.save()
            if obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):    

    def get_object(self, pk):
        try:
            return Project.objects.get(id=pk)
        except Project.DoesNotExist:
            raise Http404

    
    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ProjectSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ProjectSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectXUserList(APIView):

    def get(self, request, format=None):

        objs = ProjectXUser.objects.all()

        serializer = ProjectXUserSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectXUserSerializer(data=request.data)
        
        if serializer.is_valid():
            obj = serializer.save()
            if obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunityList(APIView):

    def get(self, request, format=None):
        objs = Community.objects.all()
        serializer = CommunitySerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommunitySerializer(data=request.data)
        
        if serializer.is_valid():
            obj = serializer.save()
            if obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommunityDetail(APIView):    

    def get_object(self, pk):
        try:
            return Community.objects.get(id=pk)
        except Community.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = CommunitySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = CommunitySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectXUniversityList(APIView):

    def get(self, request, format=None):
        objs = ProjectXUniversity.objects.all()
        serializer = ProjectXUniversitySerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectXUniversitySerializer(data=request.data)
        
        if serializer.is_valid():
            obj = serializer.save()
            if obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectXUniversityDetail(APIView):    

    def get_object(self, pk):
        try:
            return ProjectXUniversity.objects.get(id=pk)
        except ProjectXUniversity.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ProjectXUniversitySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ProjectXUniversitySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectXCommunityList(APIView):

    def get(self, request, format=None):
        objs = ProjectXCommunity.objects.all()
        serializer = ProjectXCommunitySerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectXCommunitySerializer(data=request.data)
        
        if serializer.is_valid():
            obj = serializer.save()
            if obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectXCommunityDetail(APIView):    

    def get_object(self, pk):
        try:
            return ProjectXCommunity.objects.get(id=pk)
        except ProjectXCommunity.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ProjectXCommunitySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ProjectXCommunitySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class UniversityByName(APIView):
#     #permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, input_search):

#         objs = University.objects.filter(name__icontains=input_search)
#         serializer = UniversitySerializer(objs, many=True)
#         return Response(serializer.data)