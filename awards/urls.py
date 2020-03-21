from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('logout/', views.signout, {"next_page": '/'},name="signout"),
    path('', views.home , name="index"),
    path('', views.signout,name="signout"),
    path('awards/', views.awards ,name='awards'),
    path('accounts/profile/', views.profile, name="profile"),
    path('post/', views.posts, name='posts' ),
    path('success', views.success, name = 'success'),
    path('search_blog/', views.search_blog, name="search"),
    path('rating/<post>/', views.rating, name='rating'),
    path('api/blog/', views.BlogList.as_view()),
    path('api/profile/', views.ProfileList.as_view()),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)