from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
import json

from store.models import Book, UserBookRelation
# from control_app.store.serializers import BookSerializer


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', )
        self.user2 = User.objects.create(username='test_username2', )
        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=25,
                                          author_name='Author 2',
                                          owner=self.user2)

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))

        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user2,
                                                book=self.book_1)
        self.assertTrue(relation.like)
        # serializer_data = BookSerializer([self.book_1, self.book_2],
        #                                   many=True]).data
