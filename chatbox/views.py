
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from chatbox.models import ChatMessage
from chatbox.serializers import ChatboxSerializer


class ChatboxViewSet(ModelViewSet):
    queryset=ChatMessage.objects.all()
    serializer_class=ChatboxSerializer
