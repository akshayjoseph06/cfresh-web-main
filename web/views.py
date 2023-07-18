from django.shortcuts import get_object_or_404, render, reverse
from django.http.response import HttpResponseRedirect
from .forms import ContactForm
from .models import Link, Contact, Privacy, Terms, Return, About


def index(request):
    links = Link.objects.all()
    
    context= {
        "title": "C-FRESH - Fresh Fish Anywhere.",
        "links": links,
    }
    return render(request, "web/index.html", context=context)



def privacy(request):
    privacies = Privacy.objects.all()
    
    context= {
        "title": "C-FRESH - Privacy Policy",
        "privacies": privacies,
    }
    return render(request, "web/privacy.html", context=context)



def about(request):
    abouts = About.objects.all()
    
    context= {
        "title": "C-FRESH - About Us",
        "abouts": abouts,
    }
    return render(request, "web/about.html", context=context)




def contact(request):
    
    context= {
        "title": "C-FRESH - Contact Us",
    }
    return render(request, "web/contact.html", context=context)




def return_refund(request):
    refunds = Return.objects.all()
    
    context= {
        "title": "C-FRESH - Return & Refund Policy",
        "refunds": refunds,
    }
    return render(request, "web/return.html", context=context)



def terms(request):
    term = Terms.objects.all()
    
    context= {
        "title": "C-FRESH - Terms & Conditions",
        "term": term,
    }
    return render(request, "web/terms.html", context=context)