import json
import copy
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async ,async_to_sync
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import TextMessage , Room
from ChatProject.translation import translate

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        query_params = parse_qs(self.scope["query_string"].decode())
        token = query_params.get("token", [None])[0]
        if token is None:
            await self.close()
            return

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            
            self.user = await sync_to_async(User.objects.get)(id=user_id)
        except Exception:
            await self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room = await sync_to_async(Room.objects.prefetch_related("users").get)(id=self.room_id)
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await sync_to_async(cache.set)(f"user_channel_{self.user.id}", self.channel_name)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        original_msg = text_data_json['message']['text']
        # print(text_data_json) 
        # {'message': {'sender': 1, 'sender_username': 'admin', 'text': 'how are you', 'created_at': '2025-11-17T14:50:29.326Z'}}
        # Send message to room group
        await self.send_translated_msg(text_data_json)
        
        # Save original message
        # await TextMessage.objects.acreate(
        #     room_id=self.room_id,
        #     sender_id=text_data_json['message']['sender'],
        #     text=original_msg
        # )


    # Receive message from room group
    async def chat_message(self, event):
        if event["type"] == "chat.message":
            message = event["message"]
            # Send message to WebSocket
            await self.send(text_data=json.dumps(message))
    
    async def send_translated_msg(self, text_data_json):
        sender_id = text_data_json['message']['sender']
        original_text = text_data_json['message']['text']
        src_lang = self.user.primary_lng or "eng_Latn"

        # Send original message back to sender
        sender_channel = await sync_to_async(cache.get)(f"user_channel_{sender_id}")
        if sender_channel:
            await self.channel_layer.send(sender_channel, {
                "type": "chat.message",
                "message": text_data_json  # original message
            })

        # Translate for other users
        users = [u for u in self.room.users.all() if u.id != sender_id]
        for user in users:
            tgt_lang = user.primary_lng or "eng_Latn"
            translated_text = await sync_to_async(translate)(original_text, src=src_lang, tgt=tgt_lang)

            msg_copy = copy.deepcopy(text_data_json)
            msg_copy['message']['text'] = translated_text

            channel_name = await sync_to_async(cache.get)(f"user_channel_{user.id}")
            if channel_name:
                await self.channel_layer.send(channel_name, {
                    "type": "chat.message",
                    "message": msg_copy
                })
