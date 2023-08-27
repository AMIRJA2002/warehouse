from .service import StoreQueries, SectionQueries, DeviceQueries, DeviceDataQueries
from rest_framework.response import Response
from .models import Store, Section, Device
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status


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
        store = StoreQueries.get_one(id=id, user=request.user)
        serializer = self.InputSerializer(instance=store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.OutputSerializer(store).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        StoreQueries.delete_one(id=id, owner=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, id):
        store = StoreQueries.get_one(id, user=request.user)
        return Response(self.OutputSerializer(instance=store).data, status=status.HTTP_200_OK)


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
        store = SectionQueries.create_one(user=request.user, data=data.validated_data)
        return Response(self.OutputSerializer(store).data, status=status.HTTP_201_CREATED)

    def patch(self, request, id):
        store = SectionQueries.get_one(id=id, user=request.user)
        serializer = self.InputSerializer(instance=store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.OutputSerializer(store).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        SectionQueries.delete_one(id=id, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, id):
        section = SectionQueries.get_one(id, user=request.user)
        return Response(self.OutputSerializer(instance=section).data, status=status.HTTP_200_OK)


class CreateDeviceAPIView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Device
            fields = '__all__'

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Device
            fields = '__all__'

    def post(self, request):
        data = request.data.copy()
        data = self.InputSerializer(data=data)
        data.is_valid(raise_exception=True)

        store = DeviceQueries.create_one(user=request.user, data=data.validated_data)
        return Response(self.OutputSerializer(store).data, status=status.HTTP_201_CREATED)

    def patch(self, request, id):
        store = DeviceQueries.get_one(id=id, user=request.user)
        serializer = self.InputSerializer(instance=store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.OutputSerializer(store).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        DeviceQueries.delete_one(id=id, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, id):
        device = DeviceQueries.get_one(id, user=request.user)
        return Response(self.OutputSerializer(instance=device).data, status=status.HTTP_200_OK)


class GetSensorDataAPIView(APIView):
    class InputSerializer(serializers.Serializer):
        mac_address = serializers.CharField(max_length=17)

    def get(self, request):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        sensor_data = DeviceDataQueries.get_one(address=data.validated_data['mac_address'])
        return Response({'data': sensor_data})
