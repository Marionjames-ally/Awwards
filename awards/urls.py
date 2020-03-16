from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('logout/', views.signout, {"next_page": '/'},name="signout"),
    path('', views.home , name="index"),
    path('', views.signout,name="signout"),
    path('accounts/profile/', views.profile, name="profile"),
    path('post/', views.posts, name='posts' ),
]