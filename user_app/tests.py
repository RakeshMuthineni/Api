from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token



class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username" : "rakesh",
            "email" : "raki@gmail.com",
            "password" : "maheshbabu26",
            "password2": "maheshbabu26"
        }
        #when ever we are ready with data we need to post,for that we need to use client request
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="mahesh",
                                             password="maheshbabu26")

    def test_login(self):
        data = {
            "username": "mahesh",
            "password": "maheshbabu26"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="mahesh")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)