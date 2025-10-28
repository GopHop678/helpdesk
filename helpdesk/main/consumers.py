from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Подключаемся к группе 'notifications'
        self.room_group_name = 'notifications'
        # Добавляем канал в группу
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


    async def send_notification(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': message
        }))


# class WSConsumer(WebsocketConsumer):
#     def connect(self):
#         # Подключаемся к группе 'notifications'
#         # self.room_group_name = 'notifications'
#         #
#         # # Добавляем канал в группу
#         # self.channel_layer.group_add(
#         #     self.room_group_name,
#         #     self.channel_name
#         # )
#
#         self.accept()
#
#         response = json.dumps({
#             'message': 'success',
#         })
#
#         self.send(response)
#
#
#     def disconnect(self, close_code):
#         # Удаляем канал из группы при отключении
#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
