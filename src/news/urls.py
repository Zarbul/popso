from django.urls import path, include
from rest_framework import routers

from src.news.views import NewsModelView

router = routers.DefaultRouter()
router.register('news', NewsModelView)

urlpatterns = [
    path('', include(router.urls))
]
