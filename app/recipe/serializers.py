from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recipe objects"""

    # PrimaryKeyRelatedFiled may be used to represent the target of the relationship
    # using its pk. So this basically makes sure that only the related ingredient
    # objects, will return only the ids. Which we can use later on
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingredients', 'tags',
            'time_minutes', 'price', 'link',
        )

        # Prevent use from updating id
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
