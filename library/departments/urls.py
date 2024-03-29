from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet

router_v1 = DefaultRouter()
router_v1.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router_v1.urls)),
    ]
