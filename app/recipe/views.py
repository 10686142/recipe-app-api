from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers
from core.models import Tag, Ingredient, Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""

    # Objects to use for this viewset
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    # Our authentication methods
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # IMPORTANT: Not a 'BaseRecipeAttrViewSet' because this method,
    # cannot return the objects sorted by 'name', since it does not have it
    def get_queryset(self):
        """Return recipes for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    # Our authentication methods
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # This overridden method will be called when the viewset wants the model instances,
    # for this viewset. So we want to filter for only the current authenticated user
    # And this also orders the instance in reverse aplhabetical order
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # Override this to add the foreign keyed user to the tag
    def perform_create(self, serializer):
        """Create a new model"""
        serializer.save(user=self.request.user)


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""

    # Objects to use for this viewset
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    # Objects to use for this viewset
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
