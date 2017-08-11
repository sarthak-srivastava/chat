from channels import route
from channels import include
def message_handler(message):
	print(message['text'])

channel_routing = [ include("chat.routing.websocket_routing",path = r"^/chat/stream"),
include("chat.routing.custom_routing"),]


