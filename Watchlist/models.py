from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class StreamOn(models.Model):
    name = models.CharField(max_length=234)
    about = models.CharField(max_length=233)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name



class WatchList(models.Model):
    title = models.CharField(max_length=32)
    storyline = models.CharField(max_length=234)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    platform = models.ForeignKey(StreamOn,on_delete=models.CASCADE,related_name='watchlist')
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Review(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=234)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now=True)
    watchlist = models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='reviews')

    def __str__(self):
        return self.watchlist.title + " |"+ str(self.rating) + " | " + str(self.review_user)