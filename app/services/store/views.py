from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from .service import StoreQueries
from .models import Store, Section


class CreateStoreAPIView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Store
            exclude = ('owner',)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Store
            fields = '__all__'

    def post(self, request):
        data = request.data.copy()
        data = self.InputSerializer(data=data)
        data.is_valid(raise_exception=True)

        store = StoreQueries.create_one(user=request.user, data=data.validated_data)
        return Response(self.OutputSerializer(store).data, status=status.HTTP_201_CREATED)

    def patch(self, request, id):
        store = StoreQueries.get_one(id=id)
        serializer = self.InputSerializer(instance=store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.OutputSerializer(store).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        StoreQueries.delete_one(id=id, owner=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateSectionAPIView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Section
            fields = '__all__'

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Section
            fields = '__all__'

    def post(self, request):
        data = request.data.copy()
        data = self.InputSerializer(data=data)
        data.is_valid(raise_exception=True)

        store = StoreQueries.create_one(user=request.user, data=data.validated_data)
        return Response(self.OutputSerializer(store).data, status=status.HTTP_201_CREATED)

    def patch(self, request, id):
        store = StoreQueries.get_one(id=id)
        serializer = self.InputSerializer(instance=store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.OutputSerializer(store).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        StoreQueries.delete_one(id=id, owner=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
