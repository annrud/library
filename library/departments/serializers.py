import re

from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

    def validate(self, data):
        if not re.match(r'^[a-zA-Zа-яА-Я-]+$', data['name']):
            raise serializers.ValidationError(
                'Department not saved: invalid name.'
            )
        data['name'] = data['name'].capitalize()
        if Department.objects.filter(
                name=data['name'],
        ).exists():
            raise serializers.ValidationError(
                'A department with the same name already exists.'
            )
        return data

    def create(self, validated_data):
        name = validated_data['name']
        department = Department.objects.create(name=name)
        return department
