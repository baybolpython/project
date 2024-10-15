import http

from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import App, AppStors
from .serializer import AppSerializer, AppValidateSerializer, AppStorsSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet



# class AppStorDetailView(RetrieveUpdateDestroyAPIView):
#     serializer_class = AppSerializer
#     queryset = AppStors.objects.all()
#     lookup_field = 'pk'
#

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'Total': self.page.paginator.count,
            'results': data,
        })

class ApplistView(ListCreateAPIView):
    serializer_class = AppSerializer
    queryset = App.objects.all()
    pagination_class = CustomPagination

    def post(self, request):
        serializer = AppValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        name = serializer.validated_data.get('name')
        year = serializer.validated_data.get('year')
        direction = serializer.validated_data.get('direction')
        stor_id = serializer.validated_data.get('stor')
        stor = AppStors.objects.get(id=stor_id)

        apps = App.objects.create(
            name=name,
            year=year,
            direction=direction,
            stor=stor,
        )

        return Response(status=status.HTTP_201_CREATED, data={"apps_id": apps.id})



class AppStorView(ModelViewSet):
    serializer_class = AppStorsSerializer
    queryset = AppStors.objects.all()
    lookup_field = 'id'
    pagination_class = CustomPagination


@api_view(['GET', 'PUT', 'DELETE'])
def detail_api_view(request, id):
    try:
        app = App.objects.get(id=id)
        print(app)
    except App.DoesNotExist:
        data = {
            'error': "not found"
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        data = AppSerializer(app, many=False).data
        print(data)
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = AppValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        app.name = serializer.validated_data.get('name')
        app.year = serializer.validated_data.get('year')
        app.direction = serializer.validated_data.get('direction')
        app.stor = serializer.validated_data.get('stor')

        return Response(status=status.HTTP_201_CREATED, data=AppSerializer(app).data)
    elif request.method == "DELETE":
        app.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# @api_view(http_method_names=['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def list_api_view(request):
#     if request.method == 'GET':
#
#         apps = App.objects.all()
#         data = AppSerializer(apps, many=True).data
#         print(data)
#         return Response(data=data.data, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'POST':
#         serializer = AppValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         name = serializer.validated_data.get('name')
#         year = serializer.validated_data.get('year')
#         direction = serializer.validated_data.get('direction')
#         stor_id = serializer.validated_data.get('stor')
#         stor = AppStors.objects.get(id=stor_id)
#
#         apps = App.objects.create(
#             name=name,
#             year=year,
#             direction=direction,
#             stor=stor,
#         )
#         return Response(status=status.HTTP_201_CREATED, data={"apps_id": apps.id})



def index(request):
    if request.method == 'GET':
        return HttpResponse("Hello, World!")
