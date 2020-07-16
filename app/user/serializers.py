from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

# The translation system
from django.utils.translation import ugettext_lazy as _


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False  # Password could contain whitespace
    )

    # Overriden validate function
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        # Tries to authenticate with django's build in authenticate function
        # The viewsets passes the request object via context to the Serializer
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # Check if auth has failed
        if not user:
            msg = _('Unable to authenticate with provided credentials')

            # This basically raises a 400 bad request
            raise serializers.ValidationError(msg, code='authentication')

        # Now we set the 'authenticated' user object as response in attrs
        attrs['user'] = user

        # Overriding the validate() method required to return the 'attrs'
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')

        # Keyword Arguments -> kwargs:
        # Allows us to configure a few extra settings in our model serializer
        # Use this to ensure that the password "write_only" and minmum 5 characters
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # From the docs:
    # Overrides the 'create' function to add custom functionality
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        # This creates our user by using the get_user_model and
        # passing in our serialized data the the create_user function
        return get_user_model().objects.create_user(**validated_data)

    # PUT or PATCH request, PUT updates whole object, PATCH only specified fields
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # The .pop methods grabs the element and removes it as well compated to get
        # You only do need to specify a default value for if it isn't set
        password = validated_data.pop('password', None)

        # Pass it back to the super withouth the pasword
        user = super().update(instance, validated_data)

        # Is password is given than update it with the .set_password methods
        if password:
            user.set_password(password)
            user.save()

        return user
