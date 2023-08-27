from django.urls import path
from . import views


urlpatterns = [
    path('store/create/', views.CreateStoreAPIView.as_view(), name='create-store'),
    path('store/update-delete-get/<int:id>/', views.CreateStoreAPIView.as_view(), name='update-delete-store'),
    path('section/create/', views.CreateSectionAPIView.as_view(), name='create-section'),
    path('section/update-delete-get/<int:id>/', views.CreateSectionAPIView.as_view(), name='update-delete-section'),
    path('device/create/', views.CreateDeviceAPIView.as_view(), name='create-device'),
    path('device/update-delete-get/<int:id>/', views.CreateDeviceAPIView.as_view(), name='update-delete-device'),
    path('device/data/', views.GetSensorDataAPIView.as_view(), name='get-device-data'),
]
