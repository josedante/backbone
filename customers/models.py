# backbone_django_package v0: The Foundation for a Truly Digital Business
# (c) 2018 José Sáenz
# MIT License
# https://github.com/josedante/backbone

from django.db import models

class Email(models.Model):
	label = models.CharField(max_length=100, blank=True, default='', verbose_name='etiqueta')
	address = models.EmailField(max_length=191, unique=True, verbose_name='dirección')
# 	verification_code = models.CharField(max_length=64, blank=True, default='', editable=False)
	owner = models.ForeignKey('customers.Person', null=True, blank=True, on_delete=models.SET_NULL)
# 	verified = models.BooleanField(default=False, verbose_name='verificada')
# 	disabled = models.BooleanField(
# 		default=False, verbose_name='deshabilitada', help_text='Si indicó que no quiere recibir mensajes por este canal; si no suele atenderlos; o si rebotan demasiado.'
# 	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.address
	
	class Meta:
		verbose_name = 'correo electrónico'
		verbose_name_plural = 'correos electrónicos'


class Person(models.Model):
	first_name = models.CharField(max_length=63, blank=True, verbose_name='Primer Nombre')
	last_name = models.CharField(max_length=63, blank=True, verbose_name='Apellido Paterno')
# 	nick_name = models.CharField(max_length=63, blank=True, verbose_name='Apellido Materno')
# 	full_name = models.CharField(max_length=100, blank=True, verbose_name='Segundo Nombre')
	display_name = models.CharField(max_length=100, blank=True, verbose_name='Nombre visible')
# 	id_type = models.ForeignKey(PersonalIDType, null=True, blank=True, verbose_name='Tipo de Documento')
# 	id_number = models.CharField(max_length=50, blank=True, verbose_name='Número de Documento')
# 	birthdate = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Nacimiento')
	
	primary_email = models. ForeignKey(
		Email, null=True, blank=True, on_delete=models.SET_NULL,
	)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.display_name
	
	def save(self, *args, **kwargs):
		if (self.first_name == '') & (self.last_name == ''):
			parts = self.display_name.split()
			if len(parts)>1:
				self.first_name = parts[0]
				self.last_name = parts[1]
		super(Person, self).save(*args, **kwargs)


class Organization(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
# 	org_type = models.ForeignKey(OrganizationType, null=True)
# 	industry = models.ForeignKey(Industry, null=True)
# 	org_id_type = models.ForeignKey(OrganizationalIDType, null=True)
# 	id_number = models.CharField(max_length=20)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name


class Account(models.Model):
	INDIVIDUAL = 'ID'
	CORPORATE = 'CO'
	ACCOUNT_TYPES = (
		(INDIVIDUAL, 'Personal'),
		(CORPORATE, 'Corporativa'),
	)
	account_type = models.CharField(
		max_length=2,
		choices=ACCOUNT_TYPES,
		default=CORPORATE,
		verbose_name='Tipo de cuenta'
	)
	owner = models.ForeignKey(
		Person, null=True, blank=True, on_delete=models.SET_NULL,
	)
	managed = models.ForeignKey(
		Organization, null=True, blank=True, on_delete=models.SET_NULL,
	)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		if self.account_type == 'ID':
			return str(self.owner)
		if self.account_type == 'CO':
			return str(self.managed)


