from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RecipeListViewSet


router = DefaultRouter()

router.register('recipes', RecipeListViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]
