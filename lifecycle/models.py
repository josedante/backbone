# Backbone OS
# backbone_django_package
# http://www.backboneos.com/
# Version: 0.1 alpha
# 
# Copyright 2016-2018 José Sáenz
# Released under the MIT license
# https://github.com/josedante/backbone

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import json

class SessionsTrack(models.Model):
	account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	verified_ownership = models.BooleanField(default=False)
	
	last_session = models.CharField(max_length=64, verbose_name='última sesión', blank=True)
	description = models.TextField(blank=True, default='[]')
	interactions_count = models.PositiveSmallIntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def save(self, *args, **kwargs):
		her_interactions = self.interactions
		self.interactions_count = her_interactions.count()
		
		if (self.account != None) & (her_interactions.exclude(account=None).exists()):
			self.account = her_interactions.exclude(account=None).last().account
		
		if self.user != None:
			the_email, tem_is_new = Email.objects.get_or_create(address=self.user.email)
			if the_email.owner != None:
				if Account.objects.filter(owner=the_email.owner).exists():
					last_account = Account.objects.filter(owner=the_email.owner).last()
					if self.account != None:
						if (not self.verified_ownership) & (last_account == self.account):
							self.verified_ownership = True
					else:
						self.account = last_account
						self.verified_ownership = True
		
		int_no_account = her_interactions.filter(account=None)
		if (self.account != None) & ((self.user == None) | ((self.user != None) & self.verified_ownership)):
			for interaction in int_no_account:
				interaction.account = self.account
				interaction.save()
		
		super(SessionsTrack, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name = 'usuario anónimo'
		verbose_name_plural = 'usuarios anónimos'
		ordering = ['-interactions_count', '-updated_at']
	
	@property
	def interactions(self):
		interacciones = Interaction.objects.none()
		ss_ids = json.loads(self.description)
		for ss in ss_ids:
			interacciones = interacciones | Interaction.objects.filter(session=ss)
		return interacciones


class Medium(models.Model):
	name = models.CharField(max_length=100, unique=True)
	code = models.CharField(max_length=3, unique=True)
	ASYNC = 'AS'
	SYNCR = 'SC'
	SYNC_CHOICES = (
		(ASYNC, 'asíncrono'),
		(SYNCR, 'síncrono'),
	)
	synchronicity = models.CharField(max_length=2, choices=SYNC_CHOICES, default=ASYNC)
	AUDIO = 'AU'
	VIDEO = 'VD'
	TEXT = 'TX'
	IMAGE = 'IM'
	OTHER = 'OT'
	MULTIMEDIA = 'MM'
	AVAILABLE_FORMATS = (
		(AUDIO, 'audio'),
		(VIDEO, 'video'),
		(TEXT, 'texto'),
		(IMAGE, 'imágen estática'),
		(OTHER, 'otro formato'),
		(MULTIMEDIA, 'miltimedia'),
	)
	format = models.CharField(max_length=2, choices=AVAILABLE_FORMATS, default=MULTIMEDIA)
# 	PAPER
# 	SCREEN
# 	SOUND_TERMINAL
# 	NONE
# 	support
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "media"


class Channel(models.Model):
	name = models.CharField(max_length=100, unique=True)
	code = models.CharField(max_length=100, unique=True, null=True, blank=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "canales"
		verbose_name = "canal"

class TouchPointClass(models.Model):
	name = models.CharField(max_length=100, verbose_name="nombre")
	code = models.CharField(max_length=10, null=True, blank=True, verbose_name="código")
	description = models.TextField(blank=True, verbose_name="descripción")
	channel = models.ForeignKey(Channel, verbose_name="canal", on_delete=models.CASCADE)
# 	medium = models.ForeignKey(Medium, null=True, blank=True, verbose_name="medio", on_delete=models.CASCADE)
# 	app_model = models.CharField(max_length=100, blank=True)
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
	    unique_together = ('code', 'channel',)
	def __str__(self):
		return self.name + ' @ ' + str(self.channel)
	class Meta:
		verbose_name_plural = "clases de punto de contacto"
		verbose_name = "clase de punto de contacto"

class Action(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=10, unique=True, verbose_name="código")
	description = models.TextField(blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = "acciones disponibles"
		verbose_name = "acción"

class TouchPoint(models.Model):
	name = models.CharField(max_length=191, verbose_name="nombre o título")
	code = models.CharField(max_length=100, verbose_name="código")
	url = models.URLField(max_length=191, null=True, blank=True)
	destination = models.URLField(max_length=191, null=True, blank=True)
	tp_class = models.ForeignKey(TouchPointClass, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="clase de punto de contacto")
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
		
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		if self.tp_class == None:
			return self.name + ' @ ' + 'Unknown'
		return self.name + ' @ ' + str(self.tp_class.channel)
	
	class Meta:
		verbose_name = "punto de contacto"
		verbose_name_plural = "puntos de contacto"
		unique_together = ('code', 'url', 'destination')

class Interaction(models.Model):
	timestamp = models.DateTimeField(verbose_name="fecha y hora", default=timezone.now)
	account = models.ForeignKey('customers.Account', null=True, blank=True, on_delete=models.SET_NULL, verbose_name = "cuenta")
	touchpoint = models.ForeignKey(TouchPoint, null=True, blank=True, on_delete=models.SET_NULL, verbose_name = "punto de contacto")
	action = models.ForeignKey(Action, null=True, blank=True, on_delete=models.SET_NULL, verbose_name = "acción")
	locale = models.CharField(max_length=31, default="es_PE")
	session = models.CharField(max_length=64, verbose_name='sesión', blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ['-timestamp', ]
		verbose_name = "interacción"
		verbose_name_plural = "interacciones"
	
	@property
	def anonimous_client(self):
		if self.account != None:
			return None
		
		return SessionsTrack.objects.filter(last_session=self.session).last()
	
	def __str__(self):
		if self.account != None:
			return str(self.account) + ': ' + str(self.action) + ' @ ' + str(self.touchpoint)
		else:
			if self.anonimous_client != None:
				return 'Cliente ' + str(self.anonimous_client.pk) + ': ' + str(self.action) + ' @ ' + str(self.touchpoint)
			return 'Desconocido' + ': ' + str(self.action) + ' @ ' + str(self.touchpoint)
	
	def save(self, *args, **kwargs):
		if (self.account == None) & (self.session != ''):
			if Interaction.objects.filter(session=self.session).exclude(account=None).exists():
				previous_interaction = Interaction.objects.filter(session=self.session).exclude(account=None).last()
				self.account = previous_interaction.account
		
		super(Interaction, self).save(*args, **kwargs)
