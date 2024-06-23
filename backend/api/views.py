from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate


from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer, 
) # all the serializers class from serialzers.py
from api.renderers import CustomJSONRenderer


# Define a function to generate tokens for a user
def get_tokens_for_user(user):
    # Create a refresh token for the user using the user model
    refresh = RefreshToken.for_user(user)
    # Return the refresh and access tokens as a dictionary
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Define a class for user registration
class RegisterView(APIView):
    renderer_classes = [CustomJSONRenderer]

    # Define a post method to handle user registration
    def post(self, request):
        # Create a serializer object with the user registration data
        serializer = UserRegistrationSerializer(data=request.data)
        # Check if the data is valid and raise an exception if not
        serializer.is_valid(raise_exception=True)
        # Save the user with the serialized data
        user = serializer.save()
        # Generate tokens for the user
        tokens = get_tokens_for_user(user)
        response = Response(
            {"msg": "Registration successful"},
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        return response


class LoginView(APIView):
    renderer_classes = [CustomJSONRenderer]

    # Define a post method to handle user login
    def post(self, request):
        # Create a serializer object with the user login data
        serializer = UserLoginSerializer(data=request.data)
        # Check if the data is valid and raise an exception if not
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)

        if user is None:
            return Response(
                {"errors": {"non_field_errors": ["Email or password is not valid"]}},
                status=status.HTTP_404_NOT_FOUND,
            )
        token = get_tokens_for_user(user)
        # Create a response object with the success message and the tokens
        response = Response({"msg": "Log-in Successful"}, status=status.HTTP_200_OK)
        # Set cookies for the refresh and access tokens
        response.set_cookie(
            key='refresh_token',
            value=token['refresh'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        response.set_cookie(
            key='access_token',
            value=token['access'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        # Return the response
        return response

        response = Response({"msg": "Log-in Successful"}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh_token',
            value=token['refresh'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        response.set_cookie(
            key='access_token',
            value=token['access'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        return response
    


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    # Define a get method to retrieve the user profile
    def get(self, request):
        # Get the logged in user
        user = request.user
        # Create a serializer object with the user profile data
        serializer = UserProfileSerializer(user)
        # Return the serialized user profile data
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
            )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response({"message": "Success"})
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            return response
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)