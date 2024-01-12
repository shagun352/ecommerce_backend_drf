'''serializers.py'''
from rest_framework import serializers
from product.models import Product
from .models import CartItem, Cart


class CartSerializer(serializers.ModelSerializer):
    """cart serializer"""
    class Meta:
        """ class meta"""
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    """cart item serializer"""
    product_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        """class meta"""
        model = CartItem
        fields = ['product_id', 'quantity']

    def validate_product_id(self, value):
        """
        Check that the product_id corresponds to a valid Product.
        """
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        print("the product crete =",product)
        cart_item = CartItem.objects.create(
            product=product,
            cart=validated_data['cart'],
            quantity=validated_data.get('quantity', 1)  # Default to 1 if not specified
        )
        print("validated_dta",validated_data)
        print("cart item",cart_item)
        return cart_item
