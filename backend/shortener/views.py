import requests

from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
from rest_framework.generics import GenericAPIView

from shortener.serializers import URLSerializer
from shortener.models import URL
from shortener.utils import create_shorten_path


class URLsView(GenericAPIView):

    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def get(self, request):
        shorteners = self.get_queryset()
        serializer = self.serializer_class(shorteners, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        origin_url = request.data.get('url')
        try:
            url_obj = URL.objects.get(origin_url=origin_url)
            shorten_path = f'{request.get_host}/{url_obj.shorten_path}'
            data = {'shorten_path': shorten_path}
            return JsonResponse(data)
        except:
            pass

        try:
            data['shorten_path'] = create_shorten_path()
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
            shorten_path = f'{request.get_host}/{data["shorten_path"]}'
            data = {'shorten_path': shorten_path}
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)


class URLView(GenericAPIView):

    serializer_class = URLSerializer

    def get(self, request, shorten_path):
        try:
            url = URL.objects.get(shorten_path=shorten_path)
        except Exception as e:
            data = {'error': str(e)}
            return JsonResponse(data)

        if url:
            res = requests.get(url)
            if res.context:
                return render(res.context)
        data = {'error': 'Failed to request website'}
        return JsonResponse(data)
