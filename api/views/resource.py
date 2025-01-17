from rest_framework.views import APIView
from api.serializers.resource import ResourceSerializer
from api.models import Resource
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOnly, IsAdminOrManager, IsAll
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


class ResourceAPI(APIView):
    '''
        URL: http://127.0.0.1:8000/api/resources/ (GET, POST)

        URL: http://127.0.0.1:8000/api/resources/<int:pk>/ (GET, PUT, DELETE)

        GET: Everyone can access every resource

        POST: can be accessed by Admin and Manager
        - creates resources

        PUT: Admin and Manager can handle the request

        DELETE: can be access by Admin

    '''
    
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrManager()]

        if self.request.method == 'GET':
            if self.kwargs.get('pk'):  
                return [IsAll()]
            return [IsAll()]
        
        if self.request.method == 'PUT':
            return [IsAdminOrManager()]
        
        if self.request.method == 'DELETE':
            return [IsAdminOnly()]
    
    def get_object(self, pk):
        try:
            return Resource.objects.get(pk=pk)
        except Resource.DoesNotExist:
            raise Http404


    def post(self, request, format=None):
        serializer = ResourceSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "success", "msg": "Resource Created", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "msg": "Resource Not Created", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk=None, format=None):
        if pk:
            users = self.get_object(pk)
            serializer = ResourceSerializer(users)
            return Response(serializer.data)
        users = Resource.objects.filter(is_deleted=False)
        serializer = ResourceSerializer(users, many=True)
        return Response({"count": len(serializer.data),"data":serializer.data})
    
    def put(self, request, pk=None, format=None):
        if pk:
            user = self.get_object(pk)
            serializer = ResourceSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "Error", "msg":"provide the resource id"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk=None, format=None):
        if pk:
            resource = self.get_object(pk)
            resource.is_deleted = True
            resource.save()
            return Response({"status": "success", "msg": "Resource Deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"status": "Error", "msg":"provide the resource id"}, status=status.HTTP_400_BAD_REQUEST)