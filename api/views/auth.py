from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from api.serializers.auth import UserSerializer
from api.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .permissions import IsAdminOnly, IsAdminOrManager, IsAll
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


def get_tokens_for_user(user):
    '''
        creating jwt token manually, returns
        - refresh token
        - access token
    '''
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserAPI(APIView):
    '''
        URL: http://127.0.0.1:8000/api/users/ (GET, POST)

        URL: http://127.0.0.1:8000/api/users/<int:pk>/ (GET, PUT, DELETE)

        GET: Can be accessed by Admin and Manager 
        - will return the list of users and single user
        - email, username, name and role

        POST: can be accessed by Admin
        - creates user

        PUT: Admin can update any record
        - MN, EM can update their own record

        DELETE: can be access by Admin

    '''

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        '''
            Instantiates and returns the list of permissions that this view requires.
            - return [permission() for permission in self.permission_classes]
        '''

        if self.request.method == 'POST':
            return [IsAdminOnly()]

        if self.request.method == 'GET':
            if self.kwargs.get('pk'):  
                return [IsAdminOrManager()]
            return [IsAdminOrManager()]
        
        if self.request.method == 'PUT':
            return [IsAll()]
        
        if self.request.method == 'DELETE':
            return [IsAdminOnly()]


    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404


    def get(self, request, pk=None, format=None):
        if pk:
            users = self.get_object(pk)
            serializer = UserSerializer(users)
            return Response(serializer.data)
        users = User.objects.filter(is_deleted=False)
        serializer = UserSerializer(users, many=True)
        return Response({"status": "success", "count": len(serializer.data), "data":serializer.data}, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"status": "success", "msg": "User Created", "user": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "msg": "User Not Created", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None, format=None):
        '''
            Partial update can be done this method
            - Admin can update any data
            - Other users (EM, MN) will be able to update themselves
        '''

        if pk:
            request_user = request.user
            user =  self.get_object(pk)
            
            # Admin user
            if request_user.role == 'AD':
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data":serializer.data}, status=status.HTTP_200_OK)

            # other users
            if user == request.user:
                serializer = UserSerializer(user, data=request.data,  partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data":serializer.data}, status=status.HTTP_200_OK)
                return Response({"status": "error", "msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "Error", "msg":"Not permitted"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "Error", "msg":"provide the user id"}, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk=None, format=None):
        if pk:
            user = self.get_object(pk)
            user.is_deleted = True
            user.is_active = False
            user.save()
            return Response({"status": "success", "msg": "User Deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"status": "Error", "msg":"provide the user id"}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPI(APIView):
    '''
        generates jwt token on successful login
        - username
        - password

        returns:
        - refresh token
        - access token

    '''
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"status": "error", "msg": "Username or Password cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)

        if not user:
            return Response({"status": "error", "message": "Not a valid user"}, status=status.HTTP_401_UNAUTHORIZED)
    
        token = get_tokens_for_user(user)
        
        return Response({"status": "success", "message": "Login Successfully", "token": token}, status=status.HTTP_200_OK)

