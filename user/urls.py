from django.urls import path
from .views import registerPage, loginPage, logoutUser

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),

]

