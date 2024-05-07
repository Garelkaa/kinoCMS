from django.shortcuts import render, get_object_or_404
from cinema.models import Movie, Cinema, CinemaHall
from banner.models import MainBanner
from gallery.models import GalleryImage
from other.models import Promotions, Pages, News


def main(requests):
    
    movies = Movie.objects.filter(active=True)  
    upcoming_movies = Movie.objects.filter(active=False)
    banners = MainBanner.objects.all()
    
    return render(requests, 'main/index.html', context={'title': 'Головна сторінка', 'movies': movies, 'upcoming_movies': upcoming_movies, 'banners': banners})


def afisha(requests):
    movies = Movie.objects.filter(active=True) 
    return render(requests, 'main/afisha.html', context={'title': 'Афиша', 'movies': movies})


def anothertime(requests):
    movies = Movie.objects.filter(active=False) 
    return render(requests, 'main/anothertime.html', context={'title': 'Афиша скоро', 'movies': movies})


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
    