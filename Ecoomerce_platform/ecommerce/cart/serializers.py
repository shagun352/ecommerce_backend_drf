'''serializers.py'''
from rest_framework import serializers
from product.models import Product
from .models import CartItem, Cart

class CartItemSerializer(serializers.ModelSerializer):
    """the items added in the cart"""
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=True, write_only=True, source='product')
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        """ class meta """
        model = CartItem
        fields = ['product_id', 'quantity','product_name']


class CartSerializer(serializers.ModelSerializer):
    """ cart related to the user serializer """
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        """ class meta """
        model = Cart
        fields = ['id', 'user', 'total_price', 'items']

    def get_total_price(self, obj):
        """to calculate toatl price """
        return sum(item.calculate_total_cost() for item in obj.items.all())

