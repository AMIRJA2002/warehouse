from django.contrib.auth import get_user_model
from services.common.models import BaseModel
from django.db import models

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
        return f'{self.owner.name} is owner of {self.name}'


class Section(BaseModel):
    store = models.ForeignKey(Store, related_name='sections', on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    number_of_products = models.PositiveIntegerField(default=0)
    section_capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.store.name} -> {self.name}'
