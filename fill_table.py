import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kinoCMS.settings')

import django
django.setup()

from faker import Faker
from users.models import CustomUser
from cinema.models import Cinema, Movie, CinemaHall, MovieSession
from other.models import News, Promotions, Pages, ContactsPage
from django.utils import timezone



def fill_table(rows=10):
    fake = Faker()
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
        
        News.objects.create(
                title=fake.sentence(),
                created=timezone.now(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg'))  # замените на ваш путь к изображению
            )
        Promotions.objects.create(
                title=fake.sentence(),
                created=timezone.now(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg'))  # замените на ваш путь к изображению
            )
        Pages.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg'))  # замените на ваш путь к изображению
            )
        ContactsPage.objects.create(
                title=fake.sentence(),
                address=fake.address(),
                coords_x=fake.longitude(),
                coords_y=fake.latitude(),
                logo=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg'))  # замените на ваш путь к изображению
            )
        Cinema.objects.create(
                title=fake.sentence(),
                created=timezone.now(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg')),  # замените на ваш путь к изображению
                top_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg')),  # замените на ваш путь к изображению
                url_trailer="https://example.com/trailer",
                active=True
            )
        Movie.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                main_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg')),  # замените на ваш путь к изображению
                url_trailer="https://example.com/trailer",
                type=fake.random_element(elements=('3D', '2D', 'IMAX')),  # случайно выбираем тип фильма
                active=True
            )
        CinemaHall.objects.create(
                number=fake.random_int(min=1, max=10),  # случайно выбираем номер зала от 1 до 10
                description=fake.paragraph(),
                scheme_image="static/image/map.png",  # замените на ваш путь к изображению
                top_image=fake.random_element(elements=('static/image/batman.jpeg', 'static/image/jocker.jpeg', 'static/image/spider.jpeg')),  # замените на ваш путь к изображению
                cinema_id=1  # айдишник кинотеатра, в который относится этот зал
            )
        MovieSession.objects.create(
            time=fake.time(),
            price=fake.random_int(min=50, max=200),  # случайно выбираем цену от 50 до 200
            date=timezone.now().date(),
            movie_id=1,  # айдишник фильма                cinemahall_id=1  # айдишник зала
        )



if __name__ == '__main__':
    fill_table()
