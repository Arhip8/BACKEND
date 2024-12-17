from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Container, Transportation, ContainerTransportation


def index(request):
    container_name = request.GET.get("container_name", "")
    containers = Container.objects.filter(status=1)

    if container_name:
        containers = containers.filter(name__icontains=container_name)

    draft_transportation = get_draft_transportation()

    context = {
        "container_name": container_name,
        "containers": containers
    }

    if draft_transportation:
        context["containers_count"] = len(draft_transportation.get_containers())
        context["draft_transportation"] = draft_transportation

    return render(request, "containers_page.html", context)


def add_container_to_draft_transportation(request, container_id):
    container_name = request.POST.get("container_name")
    redirect_url = f"/?container_name={container_name}" if container_name else "/"

    container = Container.objects.get(pk=container_id)

    draft_transportation = get_draft_transportation()

    if draft_transportation is None:
        draft_transportation = Transportation.objects.create()
        draft_transportation.owner = get_current_user()
        draft_transportation.date_created = timezone.now()
        draft_transportation.save()

    if ContainerTransportation.objects.filter(transportation=draft_transportation, container=container).exists():
        return redirect(redirect_url)

    item = ContainerTransportation(
        transportation=draft_transportation,
        container=container
    )
    item.save()

    return redirect(redirect_url)


def container_details(request, container_id):
    context = {
        "container": Container.objects.get(id=container_id)
    }

    return render(request, "container_page.html", context)


def delete_transportation(request, transportation_id):
    if not Transportation.objects.filter(pk=transportation_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE transportations SET status=5 WHERE id = %s", [transportation_id])

    return redirect("/")


def transportation(request, transportation_id):
    if not Transportation.objects.filter(pk=transportation_id).exists():
        return render(request, "404.html")

    transportation = Transportation.objects.get(id=transportation_id)
    if transportation.status == 5:
        return render(request, "404.html")

    context = {
        "transportation": transportation,
    }

    return render(request, "transportation_page.html", context)


def get_draft_transportation():
    return Transportation.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()