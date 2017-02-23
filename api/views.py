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
    JSON API endpoint to process game requests through the following actions.

    - `ID/state/`: **Returns** the game object.
    - `new/`: Creates a new game. **Returns** the game state. Arguments:
        - rows (number of rows)
        - columns (number of columns)
        - mines (number of mines, should be less than the board size)
    - `ID/pause/`: Pauses a given game (stops time tracking). **Returns** the game state.
    - `ID/resume/`: Resumes a given game (starts time tracking). **Returns** the game state.
    - `ID/mark_as_flag/`: Set a flag mark in a given cell. **Returns** the game state. Arguments:
        - x (cell index)
        - y (cell index)
    - `ID/mark_as_question/`: Set a question mark in a given cell. **Returns** the game state. Arguments:
        - x (cell index)
        - y (cell index)
    - `ID/reveal/`: Reveals a given cell. **Returns** the game state. Arguments:
        - x (cell index)
        - y (cell index)

    The current `state` can be:

    - **new** : for a new game.
    - **started** : if the game is running.
    - **paused** : if the game is paused.
    - **timeout** : if the game finished by timeout.
    - **won** : if the player won the game.
    - **lost** : if the player lost the game.

    The `board_view` is a matrix where each cell can be:

    - an empty character if the user hasn't set a mark or revealed the cell.
    - **?** : if the user set a question mark
    - **!** : if the user set a red flag mark
    - **x** : to indicate the cell has a mine.
    - an integer (0-8) to indicate the number of adjacent mines to the cell.

    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        return Response()

    @detail_route(methods=['get'])
    def state(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['post'])
    def new(self, request, *args, **kwargs):
        serializer = GameNewSerializer(data=request.data)
        game = None
        user = models.Player.objects.first()  # Hack to use a single user for now.
        if serializer.is_valid(raise_exception=True):
            rows = serializer.validated_data['rows']
            columns = serializer.validated_data['columns']
            mines = serializer.validated_data['mines']
            game = models.Game()
            game.title = 'Game for user %s' % (user.first_name)
            board, player_board = models.Game.new_boards(rows, columns, mines)
            game.board = board
            game.player_board = player_board
            game.state = models.Game.STATE_NEW
            game.player = user
            game.resumed_timestamp = timezone.now()
            game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def pause(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def resume(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def mark_as_flag(self, request, *args, **kwargs):
        serializer = GameMarkFlagSerializer(data=request.data)
        game = self.get_object()
        if serializer.is_valid(raise_exception=True):
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game.mark_flag_at(x, y)
            game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def mark_as_question(self, request, *args, **kwargs):
        serializer = GameMarkQuestionSerializer(data=request.data)
        game = self.get_object()
        if serializer.is_valid(raise_exception=True):
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game.mark_question_at(x, y)
            game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def reveal(self, request, *args, **kwargs):
        serializer = GameRevealSerializer(data=request.data)
        game = self.get_object()
        if serializer.is_valid(raise_exception=True):
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game.reveal_at(x, y)
            if game.is_mine_at(x, y):
                game.state = models.Game.STATE_LOST
            elif game.is_all_revealed():
                game.state = models.Game.STATE_WON
            game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)
