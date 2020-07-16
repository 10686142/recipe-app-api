from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


# This takes care of the authenticated user by classes and,
# assignig that authenticated user to the request.
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer

    # Means by which the authentication happens,
    authentication_classes = (authentication.TokenAuthentication,)

    # Level of access that the user has, so he/she most only be logged in
    # No special classes for now
    permission_classes = (permissions.IsAuthenticated,)

    # Returns the user that is authenticated from the request,
    # So here you set the user object to be used by APIView
    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


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
