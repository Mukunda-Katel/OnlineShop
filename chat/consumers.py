import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        
        
        
        # for storing in database
        await self.save_message(username, self.room_name, message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,
                'timestamp':str(await self.get_current_time())
            }
        )
        
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']
        
        await self.send(text_data=json.dumps(
            {
                'message': message,
                'username':username,
                'timestamp':timestamp
            }
        ))
        
    @database_sync_to_async
    def save_message(self, username, room_name, message):
        try:
            user = User.object.get(username=username)
            room = ChatRoom.object.get(name=room_name)
            
            ChatMessage.objects.create(
                user= user,
                room = room,
                content = message 
            )
        except (User.DoesNotExist, ChatRoom.DoesNotExist):
            pass
        
    
    @database_sync_to_async
    def get_current_time(self):
        return timezone.now()
    
                
        
    