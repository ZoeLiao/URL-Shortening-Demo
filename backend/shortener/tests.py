from functools import partial

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from backend.results import (
    SUCCESS,
    DB_ERROR,
    REQUEST_ERROR
)
from shortener.models import URL
from shortener.serializers import URLSerializer


class ShortenTests(APITestCase):

    SHORTNER_URL = reverse('shortener')
    SHORT_URL = partial(reverse, 'short_url')
    TEST_URL = 'https://stackoverflow.com/'

    def teardown(self):
        URL.objects.all().delete()

    def test_create_short_url(self):
        data = {
            'origin_url': self.TEST_URL
        }
        url = self.SHORTNER_URL
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expect_result = SUCCESS
        result = response.json()
        self.assertEqual(result['result_code'], expect_result.code)
        self.assertEqual(result['result_message'], expect_result.msg)

        short_url = result['data']['short_url']
        short_path = short_url.split('/')[-1]
        obj = URL.objects.get(short_path=short_path)
        self.assertEqual(obj.origin_url, data['origin_url'])

    def test_get_html_by_short_url(self):
        # create dummy data
        data = {
            'origin_url': self.TEST_URL,
            'short_path': 'aBc1'
        }
        serializer = URLSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        url = self.SHORT_URL(kwargs={'short_path': data['short_path']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            'Stack Overflow - Where Developers Learn',
            response.content.decode()
        )

    def test_failed_to_get_html_by_short_url_without_dummy_data(self):
        # create dummy data
        data = {
            'short_path': 'aBc1'
        }
        url = self.SHORT_URL(kwargs={'short_path': data['short_path']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expect_result = DB_ERROR(detail='')
        result = response.json()
        self.assertEqual(result['result_code'], expect_result.code)
        self.assertEqual(result['result_message'], expect_result.msg)
