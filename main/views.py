from django.shortcuts import render, get_object_or_404
from cinema.models import Movie, Cinema, CinemaHall, MovieSession, Ticked
from banner.models import MainBanner
from gallery.models import GalleryImage
from other.models import Promotions, Pages, News
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q


def main(requests):
    
    movies = Movie.objects.filter(active=True)  
    upcoming_movies = Movie.objects.filter(active=False)
    banners = MainBanner.objects.all()
    
    return render(requests, 'main/index.html', context={'title': 'Головна сторінка', 'movies': movies, 'upcoming_movies': upcoming_movies, 'banners': banners})


def search(request):
    query = request.GET.get('query')
    if query:
        movies = Movie.objects.filter(Q(title_en__icontains=query) | Q(title_uk__icontains=query))
    else:
        movies = None
    return render(request, 'main/search_results.html', {'movies': movies, 'query': query})


def afisha(requests):
    movies = Movie.objects.filter(active=True) 
    return render(requests, 'main/afisha.html', context={'title': 'Афиша', 'movies': movies})


def anothertime(requests):
    movies = Movie.objects.filter(active=False) 
    return render(requests, 'main/anothertime.html', context={'title': 'Афиша скоро', 'movies': movies})


def rasspisanie(requests):
    sessions = MovieSession.objects.all().select_related('movie', 'cinemahall')
    return render(requests, 'main/rasspisanie.html', {'title': 'Рассписание','sessions': sessions})


def bronirovane(request, session_id):
    movie_session = get_object_or_404(MovieSession.objects.select_related('movie'), id=session_id)
    rows = range(1, 6)
    seats = range(1, 11)

    context = {
        "title": 'Бронирование билета',
        "session": movie_session,
        "rows": rows,
        "seats": seats,
    }
    return render(request, 'main/bronirovanie.html', context)


def get_purchased_seats(request):
    session_id = request.GET.get('session_id')
    purchased_seats = list(Ticked.objects.filter(movie_session_id=session_id).values_list('row', 'seat'))
    return JsonResponse({'purchased_seats': purchased_seats})


@csrf_exempt
def purchase_tickets(request):
    if request.method == 'POST':
        user = request.user
        session_id = request.POST.get('session_id')
        seats = json.loads(request.POST.get('seats'))
        session = get_object_or_404(MovieSession, id=session_id)

        for seat in seats:
            Ticked.objects.create(user=user, movie_session=session, row=seat['row'], seat=seat['seat'])

        return JsonResponse({'status': 'success', 'message': 'Билеты успешно куплены'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def filmpage(requests, film_id, seo_url):
    
    movies = get_object_or_404(Movie, pk=film_id)  
    gallery_instance = GalleryImage.objects.filter(gallery=movies.gallery)
    
    return render(requests, 'main/pagefilm.html', context={'title': 'Страница фильма', 'movie': movies, 'gallery': gallery_instance})


def cinemas(requests):
    cinema = Cinema.objects.all()
    
    return render(requests, 'main/cinemas.html', context={'title': 'Наши кинотеатры', 'cinemas': cinema})


def cinemapage(request, cinema_id, seo_url):
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    gallery_instance = GalleryImage.objects.filter(gallery=cinema.gallery)

    return render(request, 'main/cinemapage.html', {
        'title': 'Страница фильма',
        'cinema': cinema,
        'gallery': gallery_instance
    })
    
    
def hallpage(request, hall_id, seo_url):
    hall = get_object_or_404(CinemaHall, pk=hall_id)
    gallery_instance = GalleryImage.objects.filter(gallery=hall.gallery)

    return render(request, 'main/hallpage.html', {
        'title': 'Страница фильма',
        'hall': hall,
        'gallery': gallery_instance
    })
    

def promotions(requests):
    promoutes = Promotions.objects.all()
    
    return render(requests, 'main/promoutes.html', context={'title': 'Акции', 'promoutes': promoutes})


def promoutespage(requests, promoute_id, promoute_url):
    promoute = get_object_or_404(Promotions, pk=promoute_id)
    gallery_instance = GalleryImage.objects.filter(gallery=promoute.gallery)

    return render(requests, 'main/promoutepage.html', {
        'title': 'Страница акции',
        'promoute': promoute,
        'gallery': gallery_instance
    })
    
    
def aboutcinema(requests):
    cinema = get_object_or_404(Pages, title_uk="Про кінотеатр")
    gallery_instance = GalleryImage.objects.filter(gallery=cinema.gallery)

    
    return render(requests, 'main/aboutcinema.html', {
        'title': 'Об кинотеатре',
        'cinema': cinema,
        'gallery': gallery_instance
    })
    

def news(requests):
    news = News.objects.all()
    
    return render(requests, 'main/news.html', {
        'title': 'Новости',
        'news': news,
    })
    

def cafebar(requests):
    cafe = get_object_or_404(Pages, title_uk='Кафе-бар')
    gallery_instance = GalleryImage.objects.filter(gallery=cafe.gallery)
    
    return render(requests, 'main/cafebar.html', {
        'title': 'Кафе-бар',
        'cafe': cafe,
        'gallery': gallery_instance
    })
    
def viphall(requests):
    hall = get_object_or_404(Pages, title_uk='Віп-зала')
    gallery_instance = GalleryImage.objects.filter(gallery=hall.gallery)
    
    return render(requests, 'main/viphall.html', {
        'title': 'Кафе-бар',
        'hall': hall,
        'gallery': gallery_instance
    })
    
    
def childroom(requests):
    room = get_object_or_404(Pages, title_uk='Дитяча кімната')
    gallery_instance = GalleryImage.objects.filter(gallery=room.gallery)
    
    return render(requests, 'main/childroom.html', {
        'title': 'Дитяча кімната',
        'room': room,
        'gallery': gallery_instance
    })
    