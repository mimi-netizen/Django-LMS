from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from .models import VirtualClassroom, ChatMessage

class ClassroomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'classroom_{self.room_name}'

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

    async def receive_json(self, content):
        message_type = content.get('type')
        if message_type == 'chat_message':
            await self.handle_chat_message(content)
        elif message_type == 'whiteboard_data':
            await self.handle_whiteboard_data(content)
        elif message_type == 'recording_started':
            await self.handle_recording_signal(content)
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_message',
                    'message': content
                }
            )

    async def handle_chat_message(self, data):
        message = data.get('message')
        if message:
            # Save chat message to database
            chat_message = await self.save_chat_message(message)
            # Broadcast to all participants
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.scope['user'].username
                }
            )

    async def handle_whiteboard_data(self, data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'whiteboard_message',
                'data': data['data'],
                'action': data['action']
            }
        )

    async def handle_recording_signal(self, data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'recording_message',
                'action': data['action']
            }
        )

    async def whiteboard_message(self, event):
        await self.send_json({
            'type': 'whiteboard_data',
            'data': event['data'],
            'action': event['action']
        })

    async def recording_message(self, event):
        await self.send_json({
            'type': 'recording_signal',
            'action': event['action']
        })

    async def chat_message(self, event):
        await self.send_json({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender']
        })

    async def broadcast_message(self, event):
        await self.send_json(event['message'])
