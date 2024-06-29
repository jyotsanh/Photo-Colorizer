from django.urls import path
# Import the user views
from .views import *  # Import the user views from the api.views.user_views module

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', UserView.as_view(), name='profile'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('upload', ImageUploadView.as_view(), name='image-upload'),
    

]
