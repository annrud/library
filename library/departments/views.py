from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    ViewSet для получения списка отделов,
    создания или удаления отдела.
    """
    @extend_schema(responses=DepartmentSerializer(many=True))
    def list(self, request, *args, **kwargs):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=DepartmentSerializer,
                   responses=DepartmentSerializer)
    def create(self, request, *args, **kwargs):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
