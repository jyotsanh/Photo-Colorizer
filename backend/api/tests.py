from django.test import TestCase

# Create your tests here.
import requests
import json

def login_test():
    URL = "http://127.0.0.1:8000/api/login"
    data = {
        'email':'ok@gmail.com',
        'password':'123'
    }
    response = requests.post(url=URL, data=data)

    if response.status_code == 200:
        # Login successful, extract tokens from the response
        # Check if the cookies are set
        if 'refresh_token' in response.cookies and 'access_token' in response.cookies:
            print("Refresh Token:", response.cookies['refresh_token'])
            print("Access Token:", response.cookies['access_token'])
        else:
            print(response.json())
    else:
        # Login failed, print error message
        print("Login failed:", response.json())

def logout_test():
    URL = "http://127.0.0.1:8000/api/logout"
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NjcxNjQzLCJpYXQiOjE3MTk2NzEzNDMsImp0aSI6IjRmZjk1OTU2Y2I5ZDRjMjg5ZTNhZDAxN2Y1NDg4MDY1IiwidXNlcl9pZCI6Mjh9.kWAW4As35Pq_ZlpAEblznA3lQdFoaEYM0fs-lkklrmY',
        
        'Content-Type': 'application/json'
    }
    data = {
        'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxOTc1Nzc0MywiaWF0IjoxNzE5NjcxMzQzLCJqdGkiOiJiZTE3NWE1YWYwNzY0NzMzYjA5ZDhmZTBmNTM2MjMyNSIsInVzZXJfaWQiOjI4fQ.R3_k7WdUlJ-E1HLJCwrE13zNa8WGQMyUDG9gJ_dJgnM'
    }
    
    response = requests.post(url=URL, headers=headers, json=data)
    print(response.json())
    
def register_test():
    url = "http://127.0.0.1:8000/api/register"
    data = {
        'email': 'testuser191@pcmgmt.edu.np',
        'username': 'testuser7911',
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
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NjY1ODA2LCJpYXQiOjE3MTk2NjU1MDYsImp0aSI6ImYwZjhmMzZlNGIxZDQ0MTNiOGE0YjIzZDUxMTRjYzQ2IiwidXNlcl9pZCI6Mjh9.Bol87OsWDRlU8jLArYDzCkMVSfcUC14asLXhkGEBtoA'
    }
    
    response = requests.get(url=URL, headers=headers)
    print(response.json())
logout_test()