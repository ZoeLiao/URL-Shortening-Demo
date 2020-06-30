import requests

from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from backend.helper import CustomJsonResponse
from backend.results import (
    SUCCESS,
    DB_ERROR,
    REQUEST_ERROR
)
from shortener.serializers import URLSerializer
from shortener.models import URL
from shortener.utils import (
    create_short_path,
    get_short_url
)


class URLsView(GenericAPIView):

    queryset = URL.objects.all()
    serializer_class = URLSerializer

    @swagger_auto_schema(
        operation_summary='Get all of the URL objects',
    )
    def get(self, request):
        shorteners = self.get_queryset()
        serializer = self.serializer_class(shorteners, many=True)
        data = serializer.data
        res = SUCCESS
        return CustomJsonResponse(res=res, data=data)

    @swagger_auto_schema(
        operation_summary='Create short URL',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'origin_url': openapi.Schema(
                     type=openapi.TYPE_STRING,
                )
            }
        )
    )
    def post(self, request):
        data = request.data
        try:
            url_obj = URL.objects.get(origin_url=data['origin_url'])
            short_url = get_short_url(request, url_obj.short_path)
            res = SUCCESS
            data = {'short_url': short_url}
            return CustomJsonResponse(res=res, data=data)
        except URL.DoesNotExist:
            pass
        except Exception as e:
            res = DB_ERROR(detail=e)
            return CustomJsonResponse(res=res)

        try:
            data['short_path'] = create_short_path()
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            short_url = get_short_url(request, data['short_path'])
            res = SUCCESS
            data = {'short_url': short_url}
            return CustomJsonResponse(res=res, data=data)
        except Exception as e:
            res = DB_ERROR(detail=e)
            return CustomJsonResponse(res=res)


class URLView(GenericAPIView):

    serializer_class = URLSerializer

    @swagger_auto_schema(
        operation_summary='Get html by short_path',
    )
    def get(self, request, short_path):
        try:
            url_obj = URL.objects.get(short_path=short_path)
        except Exception as e:
            res = DB_ERROR(detail=e)
            return CustomJsonResponse(res=res)

        if url_obj:
            res = requests.get(url_obj.origin_url)
            if res.text:
                return HttpResponse(res.text)
        data = REQUEST_ERROR(detaul='Failed to request website.')
        return CustomJsonResponse(data)
