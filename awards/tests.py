from django.test import TestCase
# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *# Create your tests here.
class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='mj', email='mj@gmail.com', password='maty122')
        self.user.save()
        self.profile_test = Profile(name="name",bio='MY bio', profile_picture='image.jpg', location='kayole', user=self.user)
        self.profile_test.save()    
    def tearDown(self) -> None:
        Profile.objects.delete().all()
        User.objects.delete().all()    
    
    def test_instance(self):
        self.profile_test.save()
        self.assertTrue(isinstance(self.profile_test, Profile))    
    def test_save_profile(self):
        self.profile_test.save()
        after = Profile.objects.all()
        self.assertTrue(len(after) > 0)
class TestBlog(TestCase):
    def setUp(self):
        self.blog_test = Blog(name='mj', image='image.png', link='https://divine.co.ke', description='test')
        self.blog_test.save()    
    def tearDown(self) -> None:
        Profile.objects.delete().all()
        User.objects.delete().all()
        Blog.objects.delete().all()    
    def test_instance(self):
        self.blog_test.save()
        self.assertTrue(isinstance(self.blog_test, Blog))    
    def test_save_image(self):
        self.blog_test.save_blog()
        blogs = Blog.objects.all()
        self.assertTrue(len(blogs) > 0)    
    def test_delete_image(self):
        self.blog_test.delete()
        after = Blog.objects.all()
        self.assertTrue(len(after) < 1)