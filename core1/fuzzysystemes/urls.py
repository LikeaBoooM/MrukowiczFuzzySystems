from django.urls import path, include
from . views import home, createOutput
from . import views
urlpatterns = [
    path('', home.as_view(), name='home'),
    path('data/', views.data, name='data'),
    path('output/', createOutput.as_view(), name='createouput'),
    path('postdata/<int:humidity>/<int:roomtemperature>/<int:oventemperature>', views.createCelcius, name='create'),
    ]