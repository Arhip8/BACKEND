from django.shortcuts import render

containers = [
    {
        "id": 1,
        "name": "Dry Freight 20",
        "description": "20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        "weight": 26,
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "Dry Freight 40",
        "description": "20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        "weight": 42,
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "High Cube 20",
        "description": "20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        "weight": 18,
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "High Cube 30",
        "description": "20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        "weight": 32,
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "High Cube 40",
        "description": "20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        "weight": 36,
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "High Cube 50",
        "description": "20-футовый контейнер увеличенного объема (за счет большей высоты и ширины). Предназначен для перевозки объёмных грузов общей массой не более 26 тонн. Позволяет разместить 3 европаллеты (шириной 800 мм) за счет сокращения глубины ребер.",
        "weight": 48,
        "image": "http://localhost:9000/images/6.png"
    }
]

draft_transportation = {
    "id": 123,
    "status": "Черновик",
    "date_created": "12 сентября 2024г",
    "vehicle": "Грузовик",
    "containers": [
        {
            "id": 1,
            "count": 2
        },
        {
            "id": 2,
            "count": 4
        },
        {
            "id": 3,
            "count": 1
        }
    ]
}


def getContainerById(container_id):
    for container in containers:
        if container["id"] == container_id:
            return container


def getContainers():
    return containers


def searchContainers(container_name):
    res = []

    for container in containers:
        if container_name.lower() in container["name"].lower():
            res.append(container)

    return res


def getDraftTransportation():
    return draft_transportation


def getTransportationById(transportation_id):
    return draft_transportation


def index(request):
    container_name = request.GET.get("container_name", "")
    containers = searchContainers(container_name) if container_name else getContainers()
    draft_transportation = getDraftTransportation()

    context = {
        "containers": containers,
        "container_name": container_name,
        "containers_count": len(draft_transportation["containers"]),
        "draft_transportation": draft_transportation
    }

    return render(request, "containers_page.html", context)


def container(request, container_id):
    context = {
        "id": container_id,
        "container": getContainerById(container_id),
    }

    return render(request, "container_page.html", context)


def transportation(request, transportation_id):
    transportation = getTransportationById(transportation_id)
    containers = [
        {**getContainerById(container["id"]), "count": container["count"]}
        for container in transportation["containers"]
    ]

    context = {
        "transportation": transportation,
        "containers": containers
    }

    return render(request, "transportation_page.html", context)
