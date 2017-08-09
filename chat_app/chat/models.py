from django.db import models
from django.utils.six import python_2_unicode_compatible
@python_2_unicode_compatible 
class Room(models.Model):
	"""A room for people to talk in """
	title = models.CharField(max_length=350)
	staff_only = models.BooleanField(default = False)
	def str(self):
		return self.title
		
