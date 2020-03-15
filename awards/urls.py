from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('index/', views.home , name="index"),
]