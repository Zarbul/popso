from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django_filters import rest_framework as filters
from src.news.models import News
from src.news.serializer import NewsSerializer


class NewsModelView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows everyone to read news
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('channel', 'tag')  # поля, по которым надо сделать фильтр
