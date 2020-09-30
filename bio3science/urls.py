
from django.urls import include, path

from . import views


app_name = 'api'
urlpatterns = [
    path('', views.HelloBio3science.as_view(), name='index'),
    path('account', views.AccountList.as_view(), name='user-list'),
    path('account/<int:pk>', views.AccountDetail.as_view(), name='user-detail'),
    path('place/<str:input_search>', views.Place.as_view(), name='place'),
    path('email-disponible/<str:email>', views.AccountByEmail.as_view(), name='email-disponible'),
    path('degree', views.DegreeList.as_view(), name='degree-list'),
    path('fields-of-study', views.FieldsOfStudyList.as_view(), name='fields-of-study-list'),
    path('profile', views.ProfileList.as_view(), name='profile-list'),
    

]