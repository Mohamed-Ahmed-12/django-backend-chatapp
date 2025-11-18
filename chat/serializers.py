from rest_framework import serializers
from .models import Room , TextMessage


class TextMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username')
    class Meta:
        model = TextMessage
        fields = ['text','created_at','sender','sender_username']

class RoomListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'name', 'last_message', 'created_at','group_chat']

    def get_group_chat(self, obj):
        return obj.is_group
    
    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        return TextMessageSerializer(last_msg).data if last_msg else None

        
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
