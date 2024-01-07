from .models import Product,Category
from product.serializers import ProductSerializer,CategorySerailizer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class ProductAPIView(APIView):
    def get(self,request,pk=None):
        if pk is not None:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            products = Product.objects.all()
            
            serializer = ProductSerializer(products, many=True)
            print(serializer.data)
            return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        try:
            product_id = Product.objects.get(id = pk)
            serializer = ProductSerializer(data = request.data,instance=product_id,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Product does not exist for update!"}, status=status.HTTP_404_NOT_FOUND)

        
    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"message": "Product does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        

class CategoryView(APIView):
    def get(self, request, category_slug=None):
        if category_slug is not None:
            category = get_object_or_404(Category,slug=category_slug)
            print(category)
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            print(serializer.data)
            return Response(serializer.data)
        else:
            all_products = Product.objects.all()
            product_serializer = ProductSerializer(all_products, many=True)
            response_data = {
                'all_products': product_serializer.data
            }

            return Response(response_data)

class AllCategories(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerailizer(categories, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)




