import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import TextMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": text_data_json}
        )
        await TextMessage.objects.acreate(
            room_id=self.room_id,
            sender_id=text_data_json['message']['sender'],
            text=text_data_json['message']['text']
        )


    # Receive message from room group
    async def chat_message(self, event):
        if event["type"] == "chat.message":
            message = event["message"]
            # Send message to WebSocket
            await self.send(text_data=json.dumps(message))
            
    
