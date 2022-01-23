import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.messages = []

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # --------------------------------------------
        incomingUsername = message['player']['username']

        self.messages.extend([message])
        for savedMessage in self.messages:
            # print(savedMessage['player']['username'])
            if (savedMessage['player']['username'] == incomingUsername):
                # print(incomingUsername + 'is already in the list')
                # print(self.messages)
                res = [x for x, z in enumerate(self.messages) if z['player']['username'] == incomingUsername]
                # print('indexes to remove at found: ' + str(len(res)))
                res.reverse()
                for index in res:
                    # print('removing message with index: ' + str(index))
                    self.messages.pop(index)

        self.messages.extend([message])
        # print(self.messages)
        # --------------------------------------------

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': self.messages
        }))
