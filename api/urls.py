from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet


router = DefaultRouter()

router.register(r'todos', TaskViewSet, basename='todo')

urlpatterns = [
    path('/api', include(router.urls)),
]

'''
DRF's DefaultRouter will automatically generate the URL patterns for the TaskView
GET    /api/todos/              - List all todos
POST   /api/todos/              - Create new todo
GET    /api/todos/{id}/         - Retrieve specific todo
PUT    /api/todos/{id}/         - Update specific todo (full)
PATCH  /api/todos/{id}/         - Update specific todo (partial)
DELETE /api/todos/{id}/         - Delete specific todo
GET    /api/todos/completed/    - Custom: Get completed todos
GET    /api/todos/pending/      - Custom: Get pending todos
POST   /api/todos/{id}/toggle_complete/ - Custom: Toggle completion
'''
