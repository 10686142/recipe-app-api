from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

# Register the our viewset with the rest_framework's default router,
# which manages all the different endpoints from the viewset for us.
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    # So all the urls from the router will be added into this path
    # which also means if you add new methods to you viewsets, it will be added
    path('', include(router.urls)),
]
