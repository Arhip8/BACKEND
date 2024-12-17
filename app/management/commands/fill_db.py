from django.conf import settings
from django.core.management.base import BaseCommand
from minio import Minio

from .utils import *
from app.models import *


def add_users():
    User.objects.create_user("user", "user@user.com", "1234", first_name="user", last_name="user")
    User.objects.create_superuser("root", "root@root.com", "1234", first_name="root", last_name="root")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234", first_name=f"user{i}", last_name=f"user{i}")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234", first_name=f"user{i}", last_name=f"user{i}")


def add_containers():
    Container.objects.create(
        name="Dry Freight 20",
        description="20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        weight=26,
        image="1.png"
    )

    Container.objects.create(
        name="Dry Freight 40",
        description="20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        weight=42,
        image="2.png"
    )

    Container.objects.create(
        name="High Cube 20",
        description="20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        weight=18,
        image="3.png"
    )

    Container.objects.create(
        name="High Cube 30",
        description="20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        weight=32,
        image="4.png"
    )

    Container.objects.create(
        name="High Cube 40",
        description="20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        weight=36,
        image="5.png"
    )

    Container.objects.create(
        name="High Cube 50",
        description="20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        weight=48,
        image="6.png"
    )

    client = Minio(settings.MINIO_ENDPOINT,
                   settings.MINIO_ACCESS_KEY,
                   settings.MINIO_SECRET_KEY,
                   secure=settings.MINIO_USE_HTTPS)

    for i in range(1, 7):
        client.fput_object(settings.MINIO_MEDIA_FILES_BUCKET, f'{i}.png', f"app/static/images/{i}.png")

    client.fput_object(settings.MINIO_MEDIA_FILES_BUCKET, 'default.png', "app/static/images/default.png")


def add_transportations():
    users = User.objects.filter(is_staff=False)
    moderators = User.objects.filter(is_staff=True)
    containers = Container.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        owner = random.choice(users)
        add_transportation(status, containers, owner, moderators)

    add_transportation(1, containers, users[0], moderators)
    add_transportation(2, containers, users[0], moderators)


def add_transportation(status, containers, owner, moderators):
    transportation = Transportation.objects.create()
    transportation.status = status

    if status in [3, 4]:
        transportation.moderator = random.choice(moderators)
        transportation.date_complete = random_date()
        transportation.date_formation = transportation.date_complete - random_timedelta()
        transportation.date_created = transportation.date_formation - random_timedelta()
    else:
        transportation.date_formation = random_date()
        transportation.date_created = transportation.date_formation - random_timedelta()

    if status == 3:
        transportation.date = random_date()

    transportation.vehicle = "Грузовик"

    transportation.owner = owner

    for container in random.sample(list(containers), 3):
        item = ContainerTransportation(
            transportation=transportation,
            container=container,
            count=random.randint(1, 10)
        )
        item.save()

    transportation.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_containers()
        add_transportations()
