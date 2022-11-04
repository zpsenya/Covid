from django.urls import path
from application import views
from application.views import *

urlpatterns = [
    path('', views.index),
    path('home/', views.index, name="home"),
    path('about/', views.about, name="about"),

    path('user/', views.user_page_view, name="user"),
    path('send_email/<int:pk>', client_send_email_view, name="send_email"),

    path('clients/', views.client_list_page_view, name="clients"),
    path('create_client/', views.client_create_form_view, name="create_client"),
    path('clients/<int:pk>', views.client_detail_page_view, name="client_detail"),
    path('client_edit/<int:pk>', views.client_edit, name="client_edit"),
    path('clients/client_delete/<int:pk>', views.client_delete_view, name="client_delete"),

    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', user_logout_view, name="logout"),

    path('pdf_view/<int:pk>', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/<int:pk>', views.DownloadPDF.as_view(), name="pdf_download"),
]
