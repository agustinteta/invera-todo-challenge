from .models import Task
from .serializers import TaskSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        content = self.request.query_params.get('content')
        if content:
            queryset = queryset.filter(content__icontains=content)

        created_at = self.request.query_params.get('created_at')
        if created_at:
            queryset = queryset.filter(created_at__date=created_at)

        return queryset

    def perform_create(self, serializer):
        # Asociar la tarea al usuario autenticado
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'content',
                openapi.IN_QUERY,
                description="Filtrar por contenido (búsqueda parcial)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'created_at',
                openapi.IN_QUERY,
                description="Filtrar por fecha de creación (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Lista tareas filtrables por contenido y fecha."""
        return super().list(request, *args, **kwargs)
    

    @action(detail=True, methods=['put'], url_path='toggle_complete')
    @swagger_auto_schema(
        request_body=no_body,
        responses={200: openapi.Response('Tarea actualizada')}
    )
    def toggle_complete(self, request, pk=None):
        """
        Endpoint personalizado que alterna el estado de completado.
        """
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        return Response(
            {"id": task.id, "is_completed": task.is_completed},
            status=status.HTTP_200_OK
        )
