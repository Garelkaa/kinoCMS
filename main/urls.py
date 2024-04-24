from django.urls import path
from . import views
from kinoCMS import settings
from django.conf.urls.static import static

app_name = 'main'


urlpatterns = [
    path('', views.main, name='main'),   
]