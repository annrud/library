from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'year', 'count', 'department_name']

    def get_department_name(self, obj):
        """Метод, возвращающий название отдела."""
        return obj.department.name if obj.department else None
