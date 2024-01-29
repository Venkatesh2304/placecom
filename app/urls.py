from django.contrib.auth import views as auth_views
from . import views
from django.urls import include, path
 
urlpatterns = [
    path('login', views.login_view , name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('home', views.home, name='home'),
    path('register', views.register_view, name='register'),
    path('get_resume', views.get_resume , name='get-resume'),
    path("update", views.StudentFormView.as_view(), name="update")
    
]