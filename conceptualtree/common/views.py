from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import User
from common.serializers import UserSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(instance)
        return Response(serializer.data)

