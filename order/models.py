from datetime import datetime
import os
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from core.models import TimeStampedModel

def extension(filename):
	return os.path.splitext(filename)[1]

class Restraunt(TimeStampedModel):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=300, blank=True)
	owner = models.ForeignKey(User)
	longitude = models.DecimalField(blank=True, max_digits=20, decimal_places=5)
	latitude = models.DecimalField(blank=True, max_digits=20, decimal_places=5)

	def __unicode__(self):
		return self.name

class Food(TimeStampedModel):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=300)
	restraunt = models.ForeignKey(Restraunt)
	cost = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
	def photo_prefix(self):
		return ('food/' + slugify(self.restraunt) + '/' + slugify(self.name) + '/')
	def portrait_photo_upload_to(self, filename):
		return (self.photo_prefix() + 'portrait' + extension(filename))
	portrait_photo = models.ImageField('Portrait Photo (220x245)', upload_to=portrait_photo_upload_to)

	def __unicode__(self):
		return self.name

class Order(TimeStampedModel):
	restraunt = models.ForeignKey(Restraunt)
	food = models.ForeignKey(Food)
	user = models.ForeignKey(User)
	transaction_id = models.CharField(max_length=64, blank=True)

	APPROVED = 'Approved'
	REFUNDED = 'Refunded'
	CANCELED = 'Canceled'
	WAITING = 'Waiting'
	TRANSACTION_TYPES = (
		(APPROVED, APPROVED),
		(REFUNDED, REFUNDED),
		(CANCELED, CANCELED),
		(WAITING, WAITING)
	)
	status = models.CharField(max_length=200, choices=TRANSACTION_TYPES, default=WAITING)
	amount = models.IntegerField(default=1)

class Rating(TimeStampedModel):
	user = models.ForeignKey(User)
	restraunt = models.ForeignKey(Restraunt)
	description = models.CharField(max_length=1000)
	rating = models.IntegerField(default=0)