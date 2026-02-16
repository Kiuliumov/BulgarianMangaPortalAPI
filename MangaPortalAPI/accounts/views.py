from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes

from .serializers import RegisterSerializer, AccountSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    lookup_field = "username"
    permission_classes = [permissions.AllowAny]


class AddFriendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            friend = User.objects.get(username=username)
            request.user.friends.add(friend)
            return Response({"message": "Friend added"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class RemoveFriendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            friend = User.objects.get(username=username)
            request.user.friends.remove(friend)
            return Response({"message": "Friend removed"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class FriendsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = request.user.friends.all()
        serializer = AccountSerializer(friends, many=True)
        return Response(serializer.data)