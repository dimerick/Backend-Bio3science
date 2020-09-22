
from django.urls import include, path

from . import views


app_name = 'api'
urlpatterns = [
    path('', views.HelloBio3science.as_view(), name='index'),
    path('account', views.AccountList.as_view(), name='user-list'),
    path('account/<int:pk>', views.AccountDetail.as_view(), name='user-detail'),
    path('place/<str:input_search>', views.Place.as_view(), name='place'),

]