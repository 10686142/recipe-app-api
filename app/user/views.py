from rest_framework import generics
from user.serializers import UserSerializer, AuthTokenSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    # Our custom serializer that supports email as usernane for auth
    serializer_class = AuthTokenSerializer

    # This sets the renderer so we can view this endpoint in the browser
    # This grabs the default ones from the rest_framework's settings
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # Only need to specify our custom Serializer
    serializer_class = UserSerializer
