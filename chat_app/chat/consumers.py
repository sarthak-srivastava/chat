from channels.auth import channel_session_user_from_http,channel_session_user
from .models import Room
import json
from channels import Channel
from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER,NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .models import Room
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError
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
@channel_session_user
@catch_client_error
def chat_join(message):
	room =get_room_or_error(message["room"],message.user)
	if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
		room.send_message(None,message.user,MSG_TYPE_ENTER)
	room.websocket_group.add(message.reply_channel)
	message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
	message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })
@channel_session_user
@catch_client_error
def leave_chat(message):
	room = get_room_or_error(message["room"],message.user)
	if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
		room.send_message(None,message.user,MSG_TYPE_ENTER)
	room.websocket_group.discard(message.reply_channel)
	message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
	message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })
@channel_session_user
@catch_client_error
def chat_send(message):
	if int(message['text']) not in message.channel_session['rooms']:
		raise ClientError("ACCESS DENIED")
	room =get_room_or_error(message['room'],message.user)
	room.send_message(message['message'],message.user)