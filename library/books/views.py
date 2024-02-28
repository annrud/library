from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response

from books.filters import BookFilter
from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet получения отфильтрованного списка книг
    или конкретной книги, создания и удаления книги,
    полного или частичного обновления записи о книге.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def destroy(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        try:
            instance.delete()
        except ProtectedError:
            return Response(
                {'error': 'This book cannot be deleted, '
                          'because it was issued to the visitor.'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
