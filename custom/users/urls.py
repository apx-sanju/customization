from django.urls import path
from . import views

urlpatterns = [
    # Path for the index page
    path('index/', views.index, name='index'),
    
    # Path for the sign-in page
    path('sign-in/', views.sign_in, name='sign_in'),
    
    # Path for the sign-up page
    path('sign_up/', views.sign_up, name='sign_up'),
    
    # Path for logging out the user
    path('logout', views.user_logout),
    
    # Path for the user profile page
    path('profile/', views.profile, name='profile'),
]

