from django.shortcuts import render
from store.models import Product, Event
from category.models import Category

def home(request):
    products = Product.objects.all().filter(is_available=True)
    categoris = Category.objects.all()
    events = Event.objects.all()
    context = {
        'products': products,
        'categoris' : categoris,
        'events': events
    }
    return render(request, 'home.html', context=context)
