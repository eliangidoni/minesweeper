from rest_framework import serializers
import api.models as models


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ('id', 'title', 'board', 'player_board', 'state',
                  'duration_seconds', 'elapsed_seconds', 'score', 'resumed_timestamp', 'player')


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
    game_id = serializers.CharField()
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)


class GameMarkFlagSerializer(serializers.Serializer):
    game_id = serializers.CharField()
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)


class GameRevealSerializer(serializers.Serializer):
    game_id = serializers.CharField()
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
