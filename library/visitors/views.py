from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import BookInHands, Visitor
from visitors.serializers import (BookBorrowSerializer,
                                  BookInHandsCreateSerializer,
                                  BookReturnSerializer,
                                  VisitorCreateSerializer,
                                  VisitorDetailSerializer,
                                  VisitorListSerializer)


class VisitorViewSet(viewsets.ModelViewSet):
    """
    ViewSet получения списка посетителей
    или конкретного посетителя, создания и удаления посетителя,
    полного или частичного обновления записи о посетителе.
    """
    queryset = Visitor.objects.all()

    def get_serializer_class(self):
        """Определение класса сериализатора в зависимости от действия."""
        if self.action == 'list':
            return VisitorListSerializer
        elif self.action == 'retrieve':
            return VisitorDetailSerializer
        elif self.action == 'create':
            return VisitorCreateSerializer
        return VisitorDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=pk)
        try:
            instance.delete()
        except ProtectedError:
            return Response(
                {'error': 'This visitor cannot be deleted, '
                          'because he borrowed books from the library.'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BorrowBookView(APIView):
    @extend_schema(
        request=BookInHandsCreateSerializer,
        responses={201: BookBorrowSerializer},
    )
    def post(self, request, visitor):
        """Метод для записи выдачи книги посетителю."""
        data = request.data
        data['visitor'] = visitor
        serializer = BookBorrowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ReturnBookView(APIView):
    @extend_schema(request=BookInHandsCreateSerializer,
                   responses=BookReturnSerializer)
    def patch(self, request, visitor):
        """Метод добавления даты возврата книги в запись о выдаче."""
        data = request.data
        data['visitor'] = visitor
        data['return_date'] = timezone.now().date()
        book_in_hands = BookInHands.objects.filter(
            visitor=visitor, book=data['book'], return_date=None
        ).first()
        if book_in_hands is None:
            return Response(
                {'error': 'This book has been returned.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookReturnSerializer(
            instance=book_in_hands, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
