from datetime import datetime  

from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
	"""
	An abstract base class model that provides self- 
	updating "created" and "modified" fields.
	""" 
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class UserExtension(TimeStampedModel):
	user = models.ForeignKey(User)
	points = models.IntegerField(default=0)
	card = models.CharField(max_length=256, blank=True)

	def __unicode__(self):
		return self.user