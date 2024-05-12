from django.urls import path
from . import views
from kinoCMS import settings
from django.conf.urls.static import static

app_name = 'main'


urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.search, name='search_results'),
    path('afisha/', views.afisha, name='afisha'),
    path('filmpage/<int:film_id>/<slug:seo_url>', views.filmpage, name='filmpage'),
    path('afisha/anothertime/', views.anothertime, name='anothertime'),
    path('rasspisanie/', views.rasspisanie, name='rasspisanie'),   
    path('filter-sessions/', views.filter_sessions, name='filter_sessions'),  
    path('bronirovanie/<int:session_id>/', views.bronirovane, name='bronirovanie'), 
    path('purchase_tickets/', views.purchase_tickets, name='purchase_tickets'),  
    path('get_purchased_seats/', views.get_purchased_seats, name='get_purchased_seats'),
    path('cinemas/', views.cinemas, name='cinemas'),   
    path('cinemas/<int:cinema_id>/<slug:seo_url>/', views.cinemapage, name='cinemapage'),
    path('hall/<int:hall_id>/<slug:seo_url>/', views.hallpage, name='hallpage'),
    path('promoutes/', views.promotions, name='promoutes'),
    path('promoutes/<int:promoute_id>/<slug:promoute_url>/', views.promoutespage, name='promoutespage'),
    path('about-cinema/', views.aboutcinema, name='aboutcinema'),
    path('news/', views.news, name='news'),
    path('cafe-bar/', views.cafebar, name='cafebar'),
    path('vip-hall/', views.viphall, name='viphall'),
    path('child-room/', views.childroom, name='childroom'),
    path('ads/', views.childroom, name='ads'),
    path('contacts/', views.childroom, name='contacts'),
    
]