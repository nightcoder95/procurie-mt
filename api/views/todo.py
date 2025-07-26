from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Todo
from ..serializers import TodoSerializer


class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['is_completed']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_queryset(self):
        '''Function returns a list of all the todos for the currently authenticated user.'''
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        '''Function saves the todo item with the currently authenticated user.'''
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Update todo with timestamp"""
        serializer.save()
    
    # Custom actions
    @action(detail=False, methods=['get'])
    def pending(self, request):
        '''Custom action to get all pending todos.'''
        pending_todos = self.get_queryset().filter(is_completed=False)
        serializer = self.get_serializer(pending_todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        '''Custom action to get all completed todos.'''
        completed_todos = self.get_queryset().filter(is_completed=True)
        serializer = self.get_serializer(completed_todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        '''Custom action to toggle the completion status of a todo item.'''
        todo = self.get_object()
        todo.is_completed = not todo.is_completed
        todo.save()
        serializer = self.get_serializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

