import json  
from channels.generic.websocket import AsyncWebsocketConsumer  
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['roomId']
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


    @database_sync_to_async
    def save_message(self,  message):
        from .models import ChatMessage
        from django.contrib.auth.models import User
        receiver = User.objects.get(username=self.room_name) 
        sender = self.scope['user']
        
        # This is the synchronous ORM call
        return ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            content=message
        )
    async def receive(self, text_data):
        from .models import ChatMessage
        from django.contrib.auth.models import User
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']

        # Save the message in the database

        # Save the chat message
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': str(sender.date_joined)
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))
