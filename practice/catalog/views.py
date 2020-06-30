from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet


def index(request):
    return render(
        request,
        'index.html',
    )


# class OrderView(ModelViewSet):