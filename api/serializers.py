from rest_framework import serializers
import api.models as models
import json


class GameSerializer(serializers.ModelSerializer):
    board_view = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = models.Game
        fields = ('id', 'title', 'state', 'board_view',
                  'duration_seconds', 'elapsed_seconds', 'score', 'resumed_timestamp')

    def get_state(self, obj):
        return obj.get_state_display()

    def get_board_view(self, obj):
        view = []
        board = json.loads(obj.board)
        player_board = json.loads(obj.player_board)
        for i in range(len(board)):
            view_row = []
            for j in range(len(board[i])):
                if player_board[i][j] == 'v':
                    view_row.append(board[i][j])
                elif player_board[i][j] == 'h':
                    view_row.append(' ')
                else:
                    view_row.append(player_board[i][j])
            view.append(view_row)
        return view


class GameGetSerializer(serializers.Serializer):
    game_id = serializers.CharField()


class GameNewSerializer(serializers.Serializer):
    rows = serializers.IntegerField(min_value=9)
    columns = serializers.IntegerField(min_value=9)
    mines = serializers.IntegerField(min_value=1)


class GamePauseSerializer(serializers.Serializer):
    game_id = serializers.CharField()


class GameResumeSerializer(serializers.Serializer):
    game_id = serializers.CharField()


class GameMarkQuestionSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)


class GameMarkFlagSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)


class GameRevealSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
