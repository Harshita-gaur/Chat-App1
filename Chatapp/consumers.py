import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from datetime import datetime
import logging

# Set up logger
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
 
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['roomId']
        # If the room is for a group, set the group identifier, otherwise, it's a user-to-user chat
        if self.room_name == 'group':
            self.room_group_name = 'group_chat'
        else:
            self.room_group_name = f'chat_{self.room_name}'  # Direct chat for specific users

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
    def save_message(self, message):
        from .models import ChatMessage
        from django.contrib.auth.models import User

        # If the room is a group, receiver should be None
        if self.room_name == 'group':
            receiver = None  # No receiver for group messages
        else:
            try:
                receiver = User.objects.get(username=self.room_name)
            except User.DoesNotExist:
                receiver = None  # Handle cases for non-existent receiver

        sender = self.scope['user']
        return ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            content=message
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']

        # Save the message in the database
        await self.save_message(message)

        # Generate the timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Send the message to all users in the group (or to a specific receiver in direct chat)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': timestamp
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
