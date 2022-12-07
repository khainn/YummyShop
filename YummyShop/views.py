from django.shortcuts import render
from store.models import Product, Event
from category.models import Category
from django.core.paginator import Paginator

def home(request):
    products = Product.objects.all().filter(is_available=True)
    categoris = Category.objects.all()
    events = Event.objects.all()

    # paginator = Paginator(products, 3)
    # page_number = request.GET.get('page')
    # page_products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categoris' : categoris,
        'events': events
    }
    return render(request, 'home.html', context=context)
