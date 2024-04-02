from django.urls import path
from . import views
from . import auth
from django.contrib.auth.views import LogoutView
from kinoCMS import settings
from django.conf.urls.static import static

app_name = 'adminlte'


urlpatterns = [
    path('login/', auth.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('stats/', views.stats, name='stats'),
    path('banner/', views.banner, name='banner'),
    path('films/', views.films, name='film'),
    path('pagefilm/', views.page_film, name='page_film'),
    path('films/<int:film_id>', views.edit_film, name='edit_films'),
    path('cinemas/', views.cinemas, name='cinema'),
    path('cinemapage/', views.cinema_page, name='cinema_page'),
    path('cinemas/<int:cinema_id>/', views.edit_cinema, name='edit_cinema'),
    path('canemahall/', views.cinema_hall, name='cinema_hall'),
    path('news/', views.news, name='news'),
    path('news/<int:news_id>/', views.edit_news, name='edit_news'),
    path('newspage/', views.news_add, name='add_news'),
    path('sells/', views.sells, name='sells'),
    path('sells/<int:sells_id>/', views.edit_sells, name='sells'),
    path('addsells/', views.add_sells, name='add_sells'),
    path('pages/', views.pages, name='pages'),
    path('main-page/', views.main_page, name='main_page'),
    path('pages/<int:page_id>/', views.edit_pages, name='edit_pages'),
    path('contacts/', views.contacts, name='contacts'),
    path('new-page/', views.new_page, name='new_page'),
    path('users/', views.users, name='users'),
    path('spam/', views.spam, name='spam'),
    path('save_email_file/', views.save_email_file, name='save_email_file'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
