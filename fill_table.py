import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kinoCMS.settings')

import django
django.setup()

from faker import Faker
from users.models import CustomUser  # Замените `your_app` на имя вашего приложения и `YourModel` на имя вашей модели


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
            card=fake.credit_card_number(),  # Случайный номер карты
            language=fake.random_element(elements=("u", "r")),  # Случайный выбор языка
            # Другие поля вашей модели
        )



if __name__ == '__main__':
    fill_table()