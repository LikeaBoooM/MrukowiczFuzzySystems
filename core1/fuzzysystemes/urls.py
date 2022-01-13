from django.urls import path, include
from . views import home
from . import views
urlpatterns = [
    path('', home.as_view(), name='home'),
    path('data/', views.data, name='data'),
    ]