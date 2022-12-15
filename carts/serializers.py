from rest_framework import routers, serializers, viewsets

from carts.models import Cart, CartItem

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart



class CartItem(serializers.ModelSerializer):
    class Meta:
        model = CartItem