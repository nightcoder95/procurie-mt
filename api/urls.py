from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.todo import TodoViewSet
from .views.auth import AuthViewSet



router = DefaultRouter()

router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
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
