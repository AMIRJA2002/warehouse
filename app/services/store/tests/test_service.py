from services.store.service import StoreQueries
from django.contrib.auth import get_user_model
from services.store.models import Store
from django.test import TestCase
from django.http import Http404

User = get_user_model()


class TestStoreQueries(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='amir8177@gmail.com', password='123456')
        cls.store = Store.objects.create(
            owner=cls.user, name='store', address='tehran', type='cold', area=1234, length=3124, width=3235, height=21
        )

    def test_get_one_correct(self):
        store = StoreQueries.get_one(id=self.store.id)
        self.assertTrue(store)
        self.assertEqual(store.owner, self.user)

    def test_get_one_incorrect(self):
        with self.assertRaises(Http404):
            StoreQueries.get_one(id=self.store.id + 1)

    def test_create_one_correct(self):
        self.assertEqual(len([self.user]), 1)

    def test_delete_one_correct(self):
        StoreQueries.delete_one(self.store.id, self.store.owner)
        with self.assertRaises(Http404):
            StoreQueries.delete_one(self.store.id, self.store.owner)

    def test_delete_one_incorrect(self):
        with self.assertRaises(Http404):
            StoreQueries.delete_one(self.store.id+1, self.store.owner)
