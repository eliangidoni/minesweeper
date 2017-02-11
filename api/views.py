from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import APIException, PermissionDenied
import api.models as models
from rest_framework import viewsets
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from django.db.models import Q

from django.db import transaction


import uuid
from django.shortcuts import render


class GameViewSet(viewsets.ViewSet):
    """
    API endpoint to process game requests through the following actions.

    """
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        return Response()

    @list_route(methods=['get'])
    def get(self, request, *args, **kwargs):
        serializer = GameGetSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']
            game = models.Game.objects.get(pk=gid)
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def new(self, request, *args, **kwargs):
        serializer = GameNewSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            rows = serializer.validated_data['rows']
            columns = serializer.validated_data['columns']
            mines = serializer.validated_data['mines']

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def pause(self, request, *args, **kwargs):
        serializer = GamePauseSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def resume(self, request, *args, **kwargs):
        serializer = GameResumeSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def mark_as_flag(self, request, *args, **kwargs):
        serializer = GameMarkFlagSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def mark_as_question(self, request, *args, **kwargs):
        serializer = GameMarkQuestionSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def reveal(self, request, *args, **kwargs):
        serializer = GameRevealSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)
