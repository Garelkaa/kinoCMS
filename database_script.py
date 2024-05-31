import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kinoCMS.settings')
django.setup()

from django.utils import timezone
from faker import Faker
from cinema.models import Cinema, Movie, CinemaHall, MovieSession
from other.models import News, Promotions, Pages, ContactsPage
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    fake = Faker()
    create_news(fake)
    create_promotions(fake)
    create_pages(fake)
    create_contacts_page(fake)
    create_cinema(fake)
    create_movie(fake)
    create_cinema_hall(fake)
    create_movie_session(fake)

def create_news(fake):
    if not News.objects.exists():
        for _ in range(5):
            News.objects.create(
                title=fake.sentence(),
                created=timezone.now(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg'))  # замените на ваш путь к изображению
            )

def create_promotions(fake):
    if not Promotions.objects.exists():
        for _ in range(5):
            Promotions.objects.create(
                title=fake.sentence(),
                created=timezone.now(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg'))  # замените на ваш путь к изображению
            )

def create_pages(fake):
    if not Pages.objects.exists():
        for _ in range(5):
            Pages.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg'))  # замените на ваш путь к изображению
            )

def create_contacts_page(fake):
    if not ContactsPage.objects.exists():
        for _ in range(5):
            ContactsPage.objects.create(
                title=fake.sentence(),
                address=fake.address(),
                coords_x=fake.longitude(),
                coords_y=fake.latitude(),
                logo=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg'))  # замените на ваш путь к изображению
            )

def create_cinema(fake):
    if not Cinema.objects.exists():
        for _ in range(5):
            Cinema.objects.create(
                title=fake.sentence(),
                created=timezone.now(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg')),  # замените на ваш путь к изображению
                top_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg')),  # замените на ваш путь к изображению
                url_trailer="https://example.com/trailer",
                active=True
            )

def create_movie(fake):
    if not Movie.objects.exists():
        for _ in range(5):
            Movie.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg')),  # замените на ваш путь к изображению
                url_trailer="https://example.com/trailer",
                type=fake.random_element(elements=('3D', '2D', 'IMAX')),  # случайно выбираем тип фильма
                active=True
            )

def create_cinema_hall(fake):
    if not CinemaHall.objects.exists():
        for _ in range(5):
            CinemaHall.objects.create(
                number=fake.random_int(min=1, max=10),  # случайно выбираем номер зала от 1 до 10
                description=fake.paragraph(),
                scheme_image="static/image/map.png",  # замените на ваш путь к изображению
                top_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg')),  # замените на ваш путь к изображению
                cinema_id=1  # айдишник кинотеатра, в который относится этот зал
            )

def create_movie_session(fake):
    if not MovieSession.objects.exists():
        for _ in range(5):
            MovieSession.objects.create(
                time=fake.time(),
                price=fake.random_int(min=50, max=200),  # случайно выбираем цену от 50 до 200
                date=timezone.now().date(),
                movie_id=1,  # айдишник фильма
                cinemahall_id=1  # айдишник зала
            )
