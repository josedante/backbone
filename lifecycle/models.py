# backbone_django_package v0: The Foundation for a Truly Digital Business
# (c) 2018 José Sáenz
# MIT License
# https://github.com/josedante/backbone

from django.db import models
from django.contrib.auth.models import User

class Medium(models.Model):
	name = models.CharField(max_length=200, unique=True)
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
	name = models.CharField(max_length=200, unique=True)
	code = models.CharField(max_length=6, unique=True, null=True, blank=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "canales"
		verbose_name = "canal"

class TouchPointClass(models.Model):
	name = models.CharField(max_length=200, verbose_name="nombre")
	code = models.CharField(max_length=9, unique=True, null=True, blank=True, verbose_name="código")
	description = models.TextField(blank=True, verbose_name="descripción")
	channel = models.ForeignKey(Channel, verbose_name="canal", on_delete=models.CASCADE)
	medium = models.ForeignKey(Medium, null=True, blank=True, verbose_name="medio", on_delete=models.CASCADE)
	app_model = models.CharField(max_length=100, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
	    unique_together = ('name', 'channel',)
	def __str__(self):
		nombre = self.name + " @ " + self.channel.name
		return nombre
	class Meta:
		verbose_name_plural = "tipos de interacción"
		verbose_name = "tipo de interacción"

class InteractionType(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.name

class TouchPoint(models.Model):
	name = models.CharField(max_length=200, verbose_name="nombre")
	description = models.TextField(verbose_name="descripción")
	code = models.CharField(max_length=10, unique=True, verbose_name="código")
	touchpoint = models.ForeignKey(TouchPointClass, on_delete=models.CASCADE, verbose_name="punto de contacto")
	NONE = 0; SEE = 1; THINK = 2; DO = 3; CARE = 4
	FUNNEL_STAGES = (
		(NONE, 'ninguna'),
		(SEE, 'SEE'),
		(THINK, 'THINK'),
		(DO, 'DO'),
		(CARE, "CARE"),
	)
	funnel_stage = models.PositiveSmallIntegerField(choices=FUNNEL_STAGES,default=NONE)
	NINGUNO = 0; ESPECIALIDAD = 1; CATEGORIA = 2; PRODUCTO = 3; MARCA = 4; JOB = 5
	CONTENT_TYPES = (
		(NINGUNO, 'desconocido o ninguno'),
		(ESPECIALIDAD, 'especialidad'),
		(CATEGORIA, 'categoría'),
		(PRODUCTO, 'producto'),
		(MARCA, "marca"),
		(JOB, "job to be done"),
	)
	content_type = models.PositiveSmallIntegerField(choices=CONTENT_TYPES,default=NINGUNO)
# 	product = models.ForeignKey('products.Product', null=True, blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.description
	class Meta:
		verbose_name = "punto de contacto"
		verbose_name_plural = "puntos de contacto"


class Interaction(models.Model):
	date = models.DateTimeField(verbose_name="fecha y hora")
	locale = models.CharField(max_length=31, default="es_PE")
	interaction_type = models.ForeignKey(InteractionType, null=True, blank=True, on_delete=models.SET_NULL)
# 	individual_customer = models.ForeignKey('accounts.Person', on_delete=models.CASCADE)
# 	corporate_customer = models.ForeignKey('accounts.Organization', null=True, blank=True)
# 	representatives = models.ManyToManyField(EmployeeOrContractor, related_name='representative_in', null=True, blank=True)
	touchpoint = models.ForeignKey(TouchPointClass, on_delete=models.SET_NULL, null=True, blank=True)
	app_model_record_pk = models.BigIntegerField(null=True, blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
	    unique_together = ('touchpoint','app_model_record_pk')
	    ordering = ['date', 'app_model_record_pk']
	
	def __str__(self):
		customer_name = self.individual_customer.first_name + " " + self.individual_customer.fathers_name
		self_name = customer_name + " @ " + self.interaction_class_name()
		return self_name
