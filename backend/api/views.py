import base64
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.conf import settings
from PIL import Image
from django.http import HttpResponse, FileResponse


import io
from .utility import Converter

MODEL_NAME = "ArtisticModel_gen_0"
FINE_TUNE_MODEL = "ArtisticModel_gen_3"

from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer, 
    ImageUploadSerializer
) # all the serializers class from serialzers.py



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

    # Define a post method to handle user registration
    def post(self, request):
        # Create a serializer object with the user registration data
        serializer = UserRegistrationSerializer(data=request.data)
        print(request.data)
        # Check if the data is valid and raise an exception if not
        if serializer.is_valid():
        # Save the user with the serialized data
            user = serializer.save()
            # Generate tokens for the user
            tokens = get_tokens_for_user(user)
            response = Response(
                {
                    "msg": "Registration successful",
                    "token":tokens
                    },
                status=status.HTTP_201_CREATED,
            )
            return response
        else:
            return Response({
                "errors": serializer.errors,
                
                },status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    # Define a post method to handle user login
    def post(self, request):
        print(request.data)
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
            
            )
        token = get_tokens_for_user(user)
        # Create a response object with the success message and the tokens
        return Response(
            {
                "msg": "Log-in Successful",
                "token":token
                }, status=status.HTTP_200_OK
            )
        
    


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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

    def post(self, request):
        try:
            print(request.data["refresh"])
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)

            response = Response({"message": "Success"})
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            return response
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ImageUploadView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Initialize converters for both models
            artistic_model = Converter(MODEL_NAME,render_factor = 20)
            fine_tuned_model = Converter(FINE_TUNE_MODEL,render_factor=20)
            
            
            
            
            image = serializer.validated_data['image']
            img = Image.open(image)
            
            img_dir = './test_images/'
            img_path = os.path.join(img_dir, 'image.jpg')

            # Create the directory if it doesn't exist
            os.makedirs(img_dir, exist_ok=True)
            img.save(img_path)
            
            # Process with the artistic model
            artistic_result_path = artistic_model.convert(img_path,url= '')
            if not artistic_result_path:
                return Response({'msg': "Something went wrong with the artistic model."}, status=404)
            
            with open(artistic_result_path, "rb") as artistic_file:
                artistic_image_data = artistic_file.read()
                
            # Process with the fine-tuned model
            fine_tuned_result_path = fine_tuned_model.convert(img_path,url= '')
            if not fine_tuned_result_path:
                return Response({'msg': "Something went wrong with the fine-tuned model."}, status=404)

            # Read the images into memory
            
            with open(fine_tuned_result_path, "rb") as fine_tuned_file:
                fine_tuned_image_data = fine_tuned_file.read()
            
            # Convert the binary data to Base64 strings
            artistic_image_base64 = base64.b64encode(artistic_image_data).decode('utf-8')
            fine_tuned_image_base64 = base64.b64encode(fine_tuned_image_data).decode('utf-8')

            # Return the base64 strings as part of the response
            return Response({
                'artistic_image_base64': f"data:image/jpeg;base64,{artistic_image_base64}",
                'fine_tuned_image_base64': f"data:image/jpeg;base64,{fine_tuned_image_base64}"
            })
            
        return Response(serializer.errors, status=400)