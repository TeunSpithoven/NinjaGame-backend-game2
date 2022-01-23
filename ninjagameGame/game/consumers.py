import json
from channels.generic.websocket import AsyncWebsocketConsumer

messages = []

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        # remove messages

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

        messages.extend([message])
        for savedMessage in messages:
            # print(savedMessage['player']['username'])
            if (savedMessage['player']['username'] == incomingUsername):
                # print(incomingUsername + 'is already in the list')
                # print(messages)
                res = [x for x, z in enumerate(messages) if z['player']['username'] == incomingUsername]
                # print('indexes to remove at found: ' + str(len(res)))
                res.reverse()
                for index in res:
                    # print('removing message with index: ' + str(index))
                    messages.pop(index)

        messages.extend([message])
        # print(messages)
        # --------------------------------------------

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': messages
        }))
