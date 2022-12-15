from django.contrib import admin
from django.urls import path, include

from . import views

from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('carts/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),

    path('orders/', include('orders.urls')),

    path('api/add_cart/', views.add_cart, name='api_add_cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

