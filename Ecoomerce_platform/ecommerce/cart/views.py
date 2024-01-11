"""views to handle cart"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from product.models import Product
from .models import  Cart
from .serializers import  CartItemSerializer, CartSerializer


class AddToCartView(generics.CreateAPIView):
    """ add to cart view """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        print(user)
        data = self.request.data

        if 'product_id' in data and 'quantity' in data:
            product_id = data['product_id']
            print(product_id)
            quantity = data['quantity']
            products = [{'product_id': product_id, 'quantity': quantity}]
            print(products)
        elif 'products' in data:
            products = data['products']
        else:
            return Response({'detail': 'Invalid data format.'}, status=status.HTTP_400_BAD_REQUEST)
        total_cost = 0
        for product_info in products:
            product_id = product_info.get('product_id')
            print(product_id)
            quantity = product_info.get('quantity')
            print(quantity)
            if not product_id or not quantity:
                return Response({'detail': 'Invalid data. '}, status=status.HTTP_400_BAD_REQUEST)
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist as e:
                raise Http404(f"Product with ID {product_id} does not exist{e}")
            cart, created = Cart.objects.get_or_create(user=user)
            cart_item = serializer.save(cart=cart, product=product, quantity=quantity)
            total_cost += cart_item.calculate_total_cost()
            print(total_cost)
            cart.items.add(cart_item)
            cart.save()
        return Response({'detail': 'Products added to the cart successfully.', 'total_cost': total_cost},
                        status=status.HTTP_201_CREATED)

class ViewCartView(generics.RetrieveAPIView):
    """to view cart data"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        return cart
