from django.contrib.auth import get_user_model
from services.common.models import BaseModel
from datetime import datetime
from django.db import models
import random
import redis

User = get_user_model()


class Store(BaseModel):
    owner = models.ForeignKey(User, related_name='store', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    type = models.CharField(max_length=150)
    area = models.PositiveIntegerField(help_text='Based on square meters')
    length = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.owner.id} is owner of {self.name}'


class Section(BaseModel):
    store = models.ForeignKey(Store, related_name='sections', on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    number_of_products = models.PositiveIntegerField(default=0)
    section_capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.store.id} -> {self.name}'


class Device(BaseModel):
    section = models.ForeignKey(Section, related_name='devices', on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=200)
    is_enable = models.BooleanField(default=True)
    mac_address = models.CharField(max_length=17, unique=True)
    end_rent_charge = models.DateTimeField(default=datetime.now, db_index=True)

    def __str__(self):
        return f"{self.section.id}/{self.name}"


class DeviceData:
    # using redis for storing

    @classmethod
    def store_data(cls, data):
        redis_conn = redis.Redis(host='redis', port=6379)
        mac_address = cls.generate_unique_name_for_sensor_data(macaddress=data.get('MacAddress'))
        for key, value in data.items():
            redis_conn.hset(mac_address, key, value)

    @staticmethod
    def generate_unique_name_for_sensor_data(macaddress):
        macaddress = f'{macaddress}_{datetime.now()}_{random.randint(0, 100000)}'
        return macaddress
