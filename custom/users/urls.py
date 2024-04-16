from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('sign-in/', views.sign_in, name='sign_in'),  
    
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout',views.user_logout),
    path('profile/', views.profile, name='profile'),
]

