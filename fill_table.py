import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kinoCMS.settings")

import django
django.setup()

from django.utils import timezone
from users.models import CustomUser
from cinema.models import Cinema, Movie, CinemaHall, MovieSession
from other.models import MainPage, News, Promotions, Pages, ContactsPage
from gallery.models import Gallery

from django.contrib.auth.hashers import make_password

from faker import Faker

fake = Faker()

def check_empty_table(model):
    return model.objects.exists()

def get_random_image():
    images = ['batman_0gmxv4F.jpeg', 'jocker_3tZ7izb.jpeg', 'spider_aWIXwNp.jpeg']
    return random.choice(images)

def generate_cinema_data(rows=10):
    if not check_empty_table(Cinema):
        for _ in range(rows):
            Cinema.objects.create(
                title=fake.company()[:40],
                created=timezone.now(),
                description=fake.text()[:7000],
                main_image=get_random_image(),
                top_image=get_random_image(),
                url_trailer=fake.url(),
                active=True,
                seo_url=fake.word(),
                seo_title=fake.text(),
                seo_keywords=fake.text(),
                description_seo=fake.text(),
                gallery=Gallery.objects.create()  # Assuming Gallery is required
            )

def generate_movie_data(rows=10):
    if not check_empty_table(Movie):
        for _ in range(rows):
            Movie.objects.create(
                title=fake.text(max_nb_chars=40),
                description=fake.text()[:7000],
                main_image=get_random_image(),
                url_trailer=fake.url(),
                type=random.choice(['3D', '2D', 'IMAX']),
                active=True,
                seo_url=fake.word(),
                seo_title=fake.text(),
                seo_keywords=fake.text(),
                description_seo=fake.text(),
                gallery=Gallery.objects.create()  # Assuming Gallery is required
            )

def generate_cinemahall_data(rows=10):
    if not check_empty_table(CinemaHall):
        for _ in range(rows):
            CinemaHall.objects.create(
                number=fake.random_int(),
                description=fake.text()[:7000],
                scheme_image=get_random_image(),
                create_at=timezone.now(),
                top_image=get_random_image(),
                seo_url=fake.word(),
                seo_title=fake.text(),
                seo_keywords=fake.text(),
                description_seo=fake.text(),
                gallery=Gallery.objects.create(),  # Assuming Gallery is required
                cinema=Cinema.objects.order_by('?').first()  # Assuming a cinema is required
            )

def generate_mainpage_data(rows=1):
    if not check_empty_table(MainPage):
        for _ in range(rows):
            MainPage.objects.create(
                phone_number=fake.phone_number()[:13],
                seo_url=fake.word(),
                seo_title=fake.text(),
                seo_keywords=fake.text(),
                description_seo=fake.text()
            )

def generate_moviesession_data(rows=10):
    if not check_empty_table(MovieSession):
        for _ in range(rows):
            MovieSession.objects.create(
                time=fake.time(),
                price=fake.random_int(),
                date=fake.date(),
                movie=Movie.objects.order_by('?').first(),  # Assuming a movie is required
                cinemahall=CinemaHall.objects.order_by('?').first()  # Assuming a cinema hall is required
            )

def generate_news_data(rows=10):
    if not check_empty_table(News):
        for _ in range(rows):
            News.objects.create(
                title=fake.text(max_nb_chars=40),
                created=timezone.now(),
                description=fake.text()[:7000],
                main_image=get_random_image(),
                url_trailer=fake.url(),
                active=True,
                seo_url=fake.word(),
                seo_title=fake.text(),
                seo_keywords=fake.text(),
                description_seo=fake.text(),
                gallery=Gallery.objects.create()  # Assuming Gallery is required
            )

def generate_promotions_data(rows=10):
    if not check_empty_table(Promotions):
        for _ in range(rows):
            Promotions.objects.create(
                title=fake.text(max_nb_chars=40),
                created=timezone.now(),
                description=fake.text()[:7000],
                main_image=get_random_image(),
                url_trailer=fake.url(),
                active=True,
                seo_url=fake.word(),
                seo_title=fake.text(),
                seo_keywords=fake.text(),
                description_seo=fake.text(),
                gallery=Gallery.objects.create()  # Assuming Gallery is required
            )

def generate_pages_data(rows=10):
    if not check_empty_table(Pages):
        for _ in range(rows):
            Pages.objects.create(
                title=fake.text(max_nb_chars=40),
                description=fake.text()[:7000],
                main_image=get_random_image(),
                created=timezone.now(),
                active=True,
                seo_url=fake.word(),
                seo_title=fake.text(),
                seo_keywords=fake.text(),
                description_seo=fake.text(),
                gallery=Gallery.objects.create()
            )

def generate_contactspage_data(rows=10):
    if not check_empty_table(ContactsPage):
        for _ in range(rows):
            ContactsPage.objects.create(
                title=fake.text(max_nb_chars=30),
                adress=fake.address(),
                coords_x=fake.latitude(),
                coords_y=fake.longitude(),
                logo=get_random_image()
            )

def fill_table(rows=10):
    if not check_empty_table(CustomUser):

        for _ in range(rows):
            CustomUser.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                second_name=fake.last_name(),  # Добавленное поле
                gender=fake.random_element(elements=("m", "f")),  # Случайный выбор пола
                birthdate=fake.date_of_birth(),  # Случайная дата рождения
                city=fake.city(),  # Случайный город
                address=fake.address(),  # Случайный адрес
                phoneNumber=fake.phone_number()[:13],  # Случайный номер телефона
                card=fake.credit_card_number()[:16],  # Случайный номер карты
                language=fake.random_element(elements=("u", "r")),  # Случайный выбор языка
                # Другие поля вашей модели
            )
    if not CustomUser.objects.filter(is_superuser=True).exists():
        CustomUser.objects.create_superuser(
            username='bbylfgroot',
            password='admin',
        )

# Call the functions to generate data
generate_cinema_data()
generate_movie_data()
generate_cinemahall_data()
generate_moviesession_data()
generate_news_data()
generate_promotions_data()
generate_pages_data()
generate_contactspage_data()
fill_table()
generate_mainpage_data()
