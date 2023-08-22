from typing import Dict

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from .models import Store, Section

User = get_user_model()


class StoreQueries:

    @classmethod
    def get_one(cls, id: int) -> QuerySet[Store]:
        return get_object_or_404(Store, id=id)

    @classmethod
    def create_one(cls, user: User, **kwargs: Dict[str, any]) -> None:
        Store.objects.create(**kwargs['data'], owner=user)

    @classmethod
    def delete_one(cls, id: int, owner: User) -> QuerySet[Store]:
        return get_object_or_404(Store, id=id, owner=owner).delete()


class SectionQueries:

    @classmethod
    def get_one(cls, id: int) -> QuerySet[Section]:
        return get_object_or_404(Section, id=id)

    @classmethod
    def create_one(cls, user: User, **kwargs: Dict[str, any]) -> QuerySet[Section]:
        store = cls.get_one(kwargs['data'].get('id'))
        if store.owner == user:
            return Section.objects.create(**kwargs['data'])
        raise PermissionDenied

    @classmethod
    def delete_one(cls, id: int, user: User) -> bool:
        section = get_object_or_404(Section, id=id)
        if section.store.owner == user:
            section.delete()
            return True
        raise PermissionDenied
