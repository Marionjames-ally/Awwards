from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
import cloudinary.uploader
from django.dispatch import receiver
# from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = CloudinaryField('image')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return str('f{self.user.username} Profile')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


    def create_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def search_profile(self,username):
        users = User.objects.filter(username=username)
        return users

class Blog(models.Model):
    image = CloudinaryField('image', default = 'image')
    name = models.CharField(max_length=250)
    caption = models.CharField(max_length=250)
    link = models.URLField(max_length=250)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='blogs')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user} Blog'

    def save_blog(self):
        self.save()

    def delete_blog(self,id):
        self.delete(id=id)

class Rating(models.Model):
    rating = (
        (1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9, '9'),(10, '10'),
    )

    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='ratings', null=True)

    class Meta:
        get_latest_by='score'

    @classmethod
    def get_leading_blog(cls):
        post=cls.objects.latest()
        return post

    def save_rating(self):
        self.save()
    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post__id=id).all()
        return ratings

    def __str__(self):
        return f'{self.post} Rating'