from rest_framework import status, response
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from Watchlist import models

class StreamOnTestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(username="mahesh",password="maheshbabu26")
        self.token = Token.objects.get(user__username == self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token.key)

        self.stream = models.StreamOn.objects.create(name="Netflix",
                                                     about="199/month",
                                                     website="https://www.netflix.in")

    def test_streamon_create(self):
        data ={
            'name':'netflix',
            'about':'199/month',
            'website':'https://www.netflix.in'
        }
        response = self.client.post(reverse('streamon-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


    def test_streamon_list(self):
        response =self.client.get(reverse('streamon-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_streamon_ind(self):
        response= self.client.get(reverse('streamon-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mahesh",password="maheshbabu26")
        self.token = Token.objects.get(user__username == self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token.key)

        self.stream = models.StreamOn.objects.create(name="Netflix",
                                                     about="199/month",
                                                     website="https://www.netflix.in")
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title="Man on the wall",
                                                         storyline ="man watch everything",
                                                         active = True)
    def test_watchlist_create(self):
        data = {
            'platform' : self.stream,
            'title' : "Man on the wall",
            "storyline" : "man watch everything",
            "active" : True
        }
        response = self.client.post(reverse('movie-list'),data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail',args=(self.wachlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(),1)
        self.assertEqual(models.WatchList.objects.get().title,'Man on the wall')



class ReviewTestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(username="mahesh",password="maheshbabu26")
        self.token = Token.objects.get(user__username == self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token.key)

        self.stream = models.StreamOn.objects.create(name="Netflix",
                                                     about="199/month",
                                                     website="https://www.netflix.in")
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title="Man on the wall",
                                                         storyline ="man watch everything",
                                                         active = True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream,
                                                         title="Man on the wall",
                                                         storyline="man watch everything",
                                                         active=True)
        self.review = models.Review.objects.create(review_user = self.user,rating = 5,
                                                   description = "Great Movie",
                                                   watchlist =self.watchlist2, active = True)


    def test_review_create(self):

        data = {

            "review_user": self.user,
            "rating":5,
            "description":"Great Movie",
            "watchlist":self.watchlist,
            "active":True
        }
        response =self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {

            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie",
            "watchlist": self.watchlist,
            "active": True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_review_update(self):
        data = {

            "review_user": self.user,
            "rating": 4,
            "description": "Great Movie-update",
            "watchlist": self.watchlist,
            "active": True
        }

        response = self.client.post(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_review_ind(self):
        response = self.client.get(reverse('review-detail',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
