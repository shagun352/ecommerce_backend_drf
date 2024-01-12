"""views to handle cart"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer

class AddToCartView(generics.CreateAPIView):
    """ view to handle add to cart """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if cart_item:
            cart_item.save()
            return Response({
                'message': 'Item quantity already in cart.',
                'product_id': cart_item.product.id,
                'quantity': cart_item.quantity
            }, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)  # pass this cart to add to ceate validated_data
        return Response({
            'message': 'Product added to cart successfully.',
            'product_id': serializer.instance.product.id,
            'quantity': serializer.instance.quantity
        }, status=status.HTTP_201_CREATED)


class ViewCartView(generics.RetrieveAPIView):
    """to view cart data"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        print(user)
        cart = Cart.objects.get(user=user)
        print(cart)
        return cart
