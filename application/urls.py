from django.urls import path
from application import views
from application.views import *

urlpatterns = [
    path('', views.index),
    path('home/', views.index, name="home"),
    path('about/', views.about, name="about"),

    path('user/', views.user, name="user"),
    path('send_email/<int:pk>', send_email, name="send_email"),

    path('clients/', views.clients, name="clients"),
    path('create_client/', views.create_client, name="create_client"),
    path('clients/<int:pk>', views.client_detail, name="client_detail"),
    path('client_edit/<int:pk>', views.client_edit, name="client_edit"),
    path('clients/client_delete/<int:pk>', views.client_delete, name="client_delete"),

    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),

    path('pdf_view/<int:pk>', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/<int:pk>', views.DownloaderPDF.as_view(), name="pdf_download"),
]
