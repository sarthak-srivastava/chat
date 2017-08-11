from django.db import models
from django.utils.six import python_2_unicode_compatible
from channels import Group
import json
from .settings import MSG_TYPE_MESSAGE
@python_2_unicode_compatible 
class Room(models.Model):
	"""A room for people to talk in """
	title = models.CharField(max_length=350)
	staff_only = models.BooleanField(default = False)
	def str(self):
		return self.title
	@property
	def websocket_group(self):
		return Group("Room-",self.id)
	def send_message(self,message,user,msg_type = MSG_TYPE_MESSAGE):
		final_msg = {'room':str(self.id),'message':message,'username':user.username,'msg_type':msg_type}
		self.websocket_group.send({"text":json.dump(final_message)})