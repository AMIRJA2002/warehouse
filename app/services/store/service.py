import json

from .models import Store, Section, Device, DeviceData
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import Http404
from typing import Dict
import redis

User = get_user_model()


class StoreQueries:

    @classmethod
    def get_one(cls, id: int, user: User) -> QuerySet[Store]:
        return get_object_or_404(Store, id=id, owner=user)

    @classmethod
    def create_one(cls, user: User, **kwargs: Dict[str, any]) -> QuerySet[Store]:
        return Store.objects.create(**kwargs['data'], owner=user)

    @classmethod
    def delete_one(cls, id: int, owner: User) -> QuerySet[Store]:
        return get_object_or_404(Store, id=id, owner=owner).delete()


class SectionQueries:

    @classmethod
    def get_one(cls, id: int, user: User) -> QuerySet[Section]:
        return get_object_or_404(Section, id=id, store__owner=user)

    @classmethod
    def create_one(cls, data: Dict[str, any], user: User) -> QuerySet[Section]:
        store = StoreQueries.get_one(id=data.get('store').id, user=user)
        if store.owner == user:
            return Section.objects.create(**data)
        raise PermissionDenied

    @classmethod
    def delete_one(cls, id: int, user: User) -> bool:
        section = get_object_or_404(Section, id=id)
        if section.store.owner == user:
            section.delete()
            return True
        raise PermissionDenied


class DeviceQueries:

    @classmethod
    def get_one(cls, id: int, user: User) -> QuerySet[Device]:
        return get_object_or_404(Device, id=id, section__store__owner=user)

    @classmethod
    def create_one(cls, user: User, data: Dict[str, any]) -> QuerySet[Device]:
        section = SectionQueries.get_one(id=data.get('section').id, user=user)
        if section.store.owner == user:
            return Device.objects.create(**data)
        raise PermissionDenied

    @classmethod
    def delete_one(cls, id: int, user: User) -> bool:
        device = get_object_or_404(Device, id=id)
        if device.section.store.owner == user:
            device.delete()
            return True
        raise PermissionDenied

    @classmethod
    def filter_by_mac_address(cls, filter_data):
        return Device.objects.filter(mac_address=filter_data)


class DeviceDataQueries:
    """
        this class using redis to store data
    """

    @classmethod
    def create_one(cls, data:Dict[any, any]) -> None:
        DeviceData.store_data(data=data)

    @classmethod
    def get_one(cls, address: str) -> list:
        redis_conn = redis.Redis(host='redis', port=6379, db=0, charset="utf-8", decode_responses=True)
        mac_address = find_all_related_hashes(address)

        sensor_data_list = []

        for i in mac_address:
            sensor_data = redis_conn.hgetall(i)
            sensor_data_list.append(sensor_data)

        if sensor_data_list:
            return sensor_data_list
        else:
            raise Http404


def find_all_related_hashes(address: str) -> set:
    redis_conn = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)
    hash_keys = redis_conn.keys('*')
    keys = set()
    for i in hash_keys:
        a = i.split('_')[0]
        if a == address:
            keys.add(i)
    return keys
