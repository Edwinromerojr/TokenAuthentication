from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage),
    path('signup/', views.signUp),
    path('test_view/', views.testView),
    path('logout/', views.logoutUser),
]