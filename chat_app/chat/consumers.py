from channels.auth import channel_session_user_from_http,channel_session_user
from .models import Room
import json
from channels import Channel

# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
	message.reply_channel.send({"accept":True})
	message.channel_session['room'] =[]
@channel_session_user
def ws_disconnect(message):
	for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(pk=room_id)
            # Removes us from the room's send group. If this doesn't get run,
            # we'll get removed once our first reply message expires.
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass
def ws_receive(message):
	payload = json.loads(message["text"])
	payload['reply_channel'] = message.content['reply_channel']
	Channel("chat.receive").send(payload)