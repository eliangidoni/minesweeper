from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import APIException, PermissionDenied
import api.models as models
from rest_framework import viewsets
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.db import transaction
import datetime
import uuid
from django.shortcuts import render


class GameViewSet(viewsets.ViewSet):
    """
    API endpoint to process game requests through the following actions.

    - `state/`: **Returns** the game state. Arguments:
        - game_id
    - `new/`: Creates a new game. **Returns** the game state. Arguments:
        - rows (number of rows)
        - columns (number of columns)
        - mines (number of mines, should be less than the board size)
    - `pause/`: Pauses a given game (stops time tracking). **Returns** the game state. Arguments:
        - game_id
    - `resume/`: Resumes a given game (starts time tracking). **Returns** the game state. Arguments:
        - game_id
    - `mark_as_flag/`: Set a flag mark in a given cell. **Returns** the game state. Arguments:
        - game_id
        - x (cell index)
        - y (cell index)
    - `mark_as_question/`: Set a question mark in a given cell. **Returns** the game state. Arguments:
        - game_id
        - x (cell index)
        - y (cell index)
    - `reveal/`: Reveals a given cell. **Returns** the game state. Arguments:
        - game_id
        - x (cell index)
        - y (cell index)

    """
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response()

    @list_route(methods=['get'])
    def state(self, request, *args, **kwargs):
        serializer = GameGetSerializer(data=request.query_params)
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
            game = models.Game()
            game.title = 'Game for user %s' % (request.user.first_name)
            board, player_board = models.Game.new_boards(rows, columns, mines)
            game.board = board
            game.player_board = player_board
            game.state = models.Game.STATE_NEW
            game.player = request.user
            game.resumed_timestamp = timezone.now()
            game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def pause(self, request, *args, **kwargs):
        serializer = GamePauseSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']
            game = models.Game.objects.get(pk=gid)
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def resume(self, request, *args, **kwargs):
        serializer = GameResumeSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']
            game = models.Game.objects.get(pk=gid)
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def mark_as_flag(self, request, *args, **kwargs):
        serializer = GameMarkFlagSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game = models.Game.objects.get(pk=gid)
            game.mark_flag_at(x, y)
            game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def mark_as_question(self, request, *args, **kwargs):
        serializer = GameMarkQuestionSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game = models.Game.objects.get(pk=gid)
            game.mark_question_at(x, y)
            game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def reveal(self, request, *args, **kwargs):
        serializer = GameRevealSerializer(data=request.data)
        game = None
        if serializer.is_valid(raise_exception=True):
            gid = serializer.validated_data['game_id']
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game = models.Game.objects.get(pk=gid)
            game.reveal_at(x, y)
            if game.is_mine_at(x, y):
                game.state = models.Game.STATE_LOST
            elif game.is_all_revealed():
                game.state = models.Game.STATE_WON
            game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)
