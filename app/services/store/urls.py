from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.CreateStoreAPIView.as_view(), name='create-store'),
    path('update/<int:id>/', views.CreateStoreAPIView.as_view(), name='update-store'),
    path('delete/<int:id>/', views.CreateStoreAPIView.as_view(), name='delete-store')
]
