from django.urls import path
from . import views
from kinoCMS import settings
from django.conf.urls.static import static

app_name = 'main'


urlpatterns = [
    path('', views.main, name='main'),
    path('afisha/', views.afisha, name='main'),
    path('afisha/anothertime/', views.anothertime, name='main'),
    path('film/<int:film_id>/<slug:seo_url>/', views.filmpage, name='filmpage'),   
    path('cinemas/', views.cinemas, name='cinemas'),   
    path('cinemas/<int:cinema_id>/<slug:seo_url>/', views.cinemapage, name='cinemapage'),
    path('hall/<int:hall_id>/<slug:seo_url>/', views.hallpage, name='hallpage'),
    path('promoutes/', views.promotions, name='promoutes'),
 
]