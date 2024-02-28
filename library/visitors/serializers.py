import re

from django.db.models import F
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from books.models import Book, BookInHands
from visitors.models import Visitor


class VisitorCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""
    class Meta:
        model = Visitor
        fields = ('id', 'first_name', 'last_name', 'address', 'phone')

    def validate_date(self, value, pattern):
        """Метод проверки введённых данных с помощью регулярного выражения."""
        return re.match(pattern, value)

    def validate(self, data):
        if not self.validate_date(data['first_name'], r'^[a-zA-Zа-яА-Я]+$'):
            raise serializers.ValidationError(
                'Visitor not saved: invalid first_name.'
            )
        if not self.validate_date(data['last_name'], r'^[a-zA-Zа-яА-Я]+$'):
            raise serializers.ValidationError(
                'Visitor not saved: invalid last_name.'
            )
        if not self.validate_date(
                data['address'], r'[/.0-9a-zA-Zа-яА-Я\s,-]+'
        ):
            raise serializers.ValidationError(
                'Visitor not saved: invalid address.'
            )
        if not self.validate_date(data['phone'], r'^\+?\d+$'):
            raise serializers.ValidationError(
                'Visitor not saved: invalid phone number.'
            )
        data['first_name'] = data['first_name'].capitalize()
        data['last_name'] = data['last_name'].capitalize()
        if self.context['request'].method == 'POST' and Visitor.objects.filter(
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
        ).exists():
            raise serializers.ValidationError(
                'This visitor is already in the database.'
            )
        return data

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        address = validated_data['address']
        phone = validated_data['phone']

        visitor = Visitor.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone
        )
        return visitor


class VisitorListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выдачи списка посетителей с количеством книг на руках.
    """
    total_book_in_hands = SerializerMethodField()

    class Meta:
        model = Visitor
        fields = (
            'id', 'first_name', 'last_name', 'total_book_in_hands'
        )

    def get_total_book_in_hands(self, obj):
        return obj.books_in_hands.filter(return_date__isnull=True).count()


class VisitorDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для выдачи информации о конкретном пользователе и книгах,
    которые он взял.
    """
    books_in_hands = serializers.SerializerMethodField()

    class Meta:
        model = Visitor
        fields = (
            'id',
            'first_name',
            'last_name',
            'address',
            'phone',
            'books_in_hands'
        )

    def get_books_in_hands(self, obj):
        """Метод получения информации о книгах, находящихся у посетителя."""
        books_in_hands = obj.books_in_hands.filter(
            return_date__isnull=True
        ).select_related('book')
        return [{
            'id': book_in_hands.book.id,
            'author': book_in_hands.book.author,
            'title': book_in_hands.book.title,
            'year of publication': book_in_hands.book.year
        } for book_in_hands in books_in_hands]


class BookInHandsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInHands
        fields = ['book']


class BookBorrowSerializer(serializers.ModelSerializer):
    """Сериализатор для создания записи о выдаче книги."""
    class Meta:
        model = BookInHands
        fields = ['id', 'visitor', 'book', 'borrow_date']

    def validate(self, data):
        book = data['book']
        visitor = data['visitor']
        if not Visitor.objects.filter(id=visitor.id).exists():
            raise serializers.ValidationError(
                'The visitor with the specified ID was not found.'
            )
        if not Book.objects.filter(id=book.id).exists():
            raise serializers.ValidationError(
                'The book with the specified ID was not found.'
            )
        elif Book.objects.get(id=book.id).count == 0:
            raise serializers.ValidationError(
                'Copies of this book are out of stock.'
            )
        return data

    def create(self, validated_data):
        """Метод создания записи о выдаче книги."""
        visitor = validated_data['visitor']
        book = validated_data['book']

        book = Book.objects.get(id=book.id)
        book.count = F('count') - 1
        book.save()

        book_in_hands = BookInHands.objects.create(
            visitor=visitor,
            book=book,
        )
        return book_in_hands


class BookReturnSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления даты возврата в запись о выдаче книги."""
    class Meta:
        model = BookInHands
        fields = ['id', 'visitor', 'book', 'borrow_date', 'return_date']

    def validate(self, data):
        """Метод проверки данных."""
        visitor = data['visitor']
        book = data['book']

        if not Visitor.objects.filter(id=visitor.id).exists():
            raise serializers.ValidationError(
                'The visitor with the specified ID was not found.'
            )
        if not Book.objects.filter(id=book.id).exists():
            raise serializers.ValidationError(
                'The book with the specified ID was not found.'
            )
        return data

    def update(self, instance, validated_data):
        """Метод обновления данных."""
        book = validated_data['book']
        book = Book.objects.get(id=book.id)
        book.count = F('count') + 1
        book.save()

        return super().update(instance=instance, validated_data=validated_data)
