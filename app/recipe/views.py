from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers
from core.models import Tag, Ingredient


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage ingredients in the database"""

    # Our authentication methods
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Objects to use for this viewset
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    # This overridden method will be called when the viewset wants the model instances,
    # for this viewset. So we want to filter for only the current authenticated user
    # And this also orders the instance in reverse aplhabetical order
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # Override this to add the foreign keyed user to the tag
    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # This overridden method will be called when the viewset wants the model instances,
    # for this viewset. So we want to filter for only the current authenticated user
    # And this also orders the instance in reverse aplhabetical order
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # Override this to add the foreign keyed user to the tag
    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)
