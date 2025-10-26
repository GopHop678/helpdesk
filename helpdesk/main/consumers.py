from channels.generic.websocket import WebsocketConsumer
import json


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        response = json.dumps({
            'message': 'success',
        })

        self.send(response)
