from django.urls import path

from web import views


app_name = "web"

urlpatterns = [
    path('', views.index, name="index"),
    path("privacy/", views.privacy, name="privacy" ),
    path("contact/", views.contact, name="contact" ),
    path("about/", views.about, name="about" ),
    path("return/", views.return_refund, name="return_refund" ),
    path("terms/", views.terms, name="terms" )
]