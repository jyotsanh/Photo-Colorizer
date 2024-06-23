from django.test import TestCase

# Create your tests here.
import requests
import json

def login_test():
    URL = "http://127.0.0.1:8000/api/login"
    data = {
        'email':'testuser01@pcmgmt.edu.np',
        'password':'password123'
    }
    response = requests.post(url=URL, data=data)

    if response.status_code == 200:
        # Login successful, extract tokens from the response
        # Check if the cookies are set
        if 'refresh_token' in response.cookies and 'access_token' in response.cookies:
            print("Refresh Token:", response.cookies['refresh_token'])
            print("Access Token:", response.cookies['access_token'])
        else:
            print("Tokens not found in cookies")
    else:
        # Login failed, print error message
        print("Login failed:", response.json())

def logout_test():
    URL = "http://127.0.0.1:8000/api/logout"
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3ODY1MDc3LCJpYXQiOjE3MTc4NjQxNzcsImp0aSI6ImVlMzNiNDIzYmExZTRjMDk4ZWY1NTg1YTYzMTRhZTY2IiwidXNlcl9pZCI6NH0.-_-1vA_gyWjHcUVS_T_9Ap2IxghnnXGzkNFW5GpTUb4',
        
        'Content-Type': 'application/json'
    }
    data = {
        'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzk1MDU3NywiaWF0IjoxNzE3ODY0MTc3LCJqdGkiOiI2NzcyOTQ1ZTljNGM0OTM4YTMyNzk0N2MwNmMzODkyMiIsInVzZXJfaWQiOjR9.n6XVD9M6Gfi3mUFJXQwSIjMW79s06dg4XJ0zqj7KnmA'
    }
    
    response = requests.post(url=URL, headers=headers, json=data)
    print(response.json())
    
def register_test():
    url = "http://127.0.0.1:8000/api/register"
    data = {
        'email': 'testuser01@pcmgmt.edu.np',
        'username': 'testuser01',
        'first_name': 'Test05',
        'last_name': 'User05',
        'password': 'password123',
        'password2': 'password123',
    }

    # Send POST request with JSON data and correct Content-Type header
    response = requests.post(url, json=data)

    # Print response
    print(response.json())
    # Check if the cookies are set
    if 'refresh_token' in response.cookies and 'access_token' in response.cookies:
        print("Refresh Token:", response.cookies['refresh_token'])
        print("Access Token:", response.cookies['access_token'])
    else:
        print("Tokens not found in cookies")

def profile_test():
    URL = "http://127.0.0.1:8000/api/profile"
    login_url = "http://127.0.0.1:8000/api/login"
    login_data = {
        'email': 'testuser01@pcmgmt.edu.np',
        'password': 'password123'
    }

    # Step 1: Log in to get the access token
    login_response = requests.post(login_url, json=login_data)
    login_response_data = login_response.json()
    print("Login Response:", login_response_data)

    # Check if login was successful and tokens were received
    if 'refresh_token' in login_response.cookies and 'access_token' in login_response.cookies:
        access_token = login_response.cookies['access_token']
        refresh_token = login_response.cookies['refresh_token']
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)

        # Step 2: Use the access token to hit the profile endpoint
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        profile_response = requests.get(URL, headers=headers)

        # Print profile response
        print("Profile Response:", profile_response.json())
    else:
        print("Login failed or tokens not found in cookies")

profile_test()