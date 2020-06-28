from django.urls import path
from . import views
urlpatterns = [
    path("", views.indexPage , name = "indexPage"),
    path("login/", views.loginPage, name="loginPage" ),
    path("adminHome/", views.adminHome, name="adminhome"),
    path('logoutUser/', views.logoutUser,name='logoutUser'),
    path('predict/', views.predict, name="predict"),
    path('prediction/', views.upredict, name="prediction"),
    path('addtoken/', views.addtoken, name="addtoken"),
    path('viewdata/', views.viewdata, name="viewdata"),
    path('about/', views.about, name="about"),
    path('aboutUs/', views.aboutUs, name="aboutUs"),
]

