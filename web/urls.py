from django.urls import path,include
from web.views import index,privacy,contact,about,return_refund,terms

app_name = "web"

urlpatterns = [
    path("", index, name="index"),
    path("privacy/", privacy, name="privacy" ),
    path("contact/", contact, name="contact" ),
    path("about/", about, name="about" ),
    path("return/", return_refund, name="return_refund" ),
    path("terms/", terms, name="terms" )

]
