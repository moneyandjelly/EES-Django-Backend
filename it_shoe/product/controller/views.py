from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from product.entity.models import Product
from product.serializers import ProductSerializer
from product.service.product_service_impl import ProductServiceImpl
from viewCount.controller.views import view_count_product_service

# Create your views here.
# viewsets를 사용하려면 rest_framework가 설정되어야 합니다.
# pip install djangorestframework
class ProductView(viewsets.ViewSet):
    queryset = Product.objects.all()
    productService = ProductServiceImpl.getInstance()

    def list(self, request):
        productList = self.productService.list()
        serializer = ProductSerializer(productList, many=True)
        return Response(serializer.data)

    def register(self, request):
        try:
            data = request.data

            productImage = request.FILES.get('productImage')
            productName = data.get('productName')
            productPrice = data.get('productPrice')
            productDescription = data.get('productDescription')

            if not all([productImage, productName, productPrice, productDescription]):
                return Response({ 'error': '모든 내용을 채워주세요!' },
                                status=status.HTTP_400_BAD_REQUEST)

            savedProduct = self.productService.createProduct(productName, productPrice,
                                              productDescription, productImage)

            serializer = ProductSerializer(savedProduct)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print('상품 등록 과정 중 문제 발생:', e)
            return Response({ 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def readProduct(self, request, pk=None):
        view_count_product_service.increment_product_view_count(pk)
        product = self.productService.readProduct(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
