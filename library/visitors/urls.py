from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BorrowBookView, ReturnBookView, VisitorViewSet

router_v1 = DefaultRouter()
router_v1.register('visitors', VisitorViewSet, basename='visitor')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'visitors/<int:visitor>/borrow/',
        BorrowBookView.as_view(),
        name='borrow-book'
    ),
    path(
        'visitors/<int:visitor>/return/',
        ReturnBookView.as_view(),
        name='return-book'
    ),
]
