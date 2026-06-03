from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .serializers import RegisterSerializer


# Create your views here.
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]