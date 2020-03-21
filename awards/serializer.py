from rest_framework import serializers
from .models import *

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('image', 'name', 'caption', 'link')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user','name', 'profile_picture', 'bio')