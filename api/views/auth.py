from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer


class AuthViewSet(ModelViewSet):
    '''Authentication ViewSet for register, login, logout, profile'''
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegistrationSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        return UserSerializer
    
    def get_permissions(self):
        '''Set permissions based on action'''
        if self.action in ['register', 'login']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        '''Register a new user'''
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        '''Login a user and return JWT tokens'''
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'message': 'User logged in successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        '''Logout a user and blacklist JWT tokens'''
        try:
          refresh_token = request.data.get('refresh_token')
          
          if not refresh_token:
                return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
          
          token = RefreshToken(refresh_token)
          token.blacklist()
          
          return Response(
                {'message': 'Successfully logged out'}, 
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {'error': 'Invalid refresh token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except:
          print('An exception occurred')
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = self.get_serializer(
            request.user, 
            data=request.data, 
            partial=request.method == 'PATCH'
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)