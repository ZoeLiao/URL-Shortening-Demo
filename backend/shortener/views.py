import requests

from django.http import (
    HttpResponse,
    JsonResponse
)
from django.shortcuts import render
from django.db import transaction
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
        return JsonResponse(data, safe=False)

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
            data = {'short_url': short_url}
            return JsonResponse(data)
        except URL.DoesNotExist:
            pass
        except Exception as e:
            data = {'error': str(e)}
            return JsonResponse(data)

        try:
            data['short_path'] = create_short_path()
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
            short_url = get_short_url(request, url_obj.short_path)
            data = {'short_url': short_url}
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)


class URLView(GenericAPIView):

    serializer_class = URLSerializer

    @swagger_auto_schema(
        operation_summary='Get html by short_path',
    )
    def get(self, request, short_path):
        try:
            url_obj = URL.objects.get(short_path=short_path)
        except Exception as e:
            data = {'error': str(e)}
            return JsonResponse(data)

        if url_obj:
            res = requests.get(url_obj.origin_url)
            if res.text:
                return HttpResponse(res.text)
        data = {'error': 'Failed to request website'}
        return JsonResponse(data)
