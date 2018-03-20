# backbone_django_package v0: The Foundation for a Truly Digital Business
# (c) 2018 José Sáenz
# MIT License
# https://github.com/josedante/backbone

from django.db import models

from lifecycle.models import *
from customers.models import *

class HelpRequest(Interaction):
	name = models.CharField(max_length=100, verbose_name='nombre')
	email = models.EmailField(max_length=191, verbose_name='correo electrónico')
	organization = models.CharField(max_length=100, verbose_name='empresa')
	problem = models.TextField(verbose_name='problema')
	
	class Meta:
		verbose_name = 'solicitud'
		verbose_name_plural = 'solicitudes'
		ordering = ['-created_at']
	
	def __str__(self):
		return self.name + ' @ ' + self.organization
	
	def save(self, *args, **kwargs):
		channel, ch_is_new = Channel.objects.get_or_create(name='Website', code='web')
		tp_class, tpc_is_new = TouchPointClass.objects.get_or_create(name='Formulario', code='form', channel=channel)
		touchpoint, tp_is_new = TouchPoint.objects.get_or_create(
			name='Solicitud de Ayuda',
			code='helpreq',
			tp_class=tp_class
		)
		i_type, it_is_new = InteractionType.objects.get_or_create(
			name='Completar Formulario',
			code='form',
		)
		if self.touchpoint != touchpoint:
			self.touchpoint = touchpoint
		if self.interaction_type != i_type:
			self.interaction_type = i_type
		the_email, tem_is_new = Email.objects.get_or_create(address=self.email)
		if the_email.owner == None:
			the_email.owner, owner_is_new = Person.objects.get_or_create(primary_email=the_email)
			the_email.save()
			if owner_is_new:
				the_email.owner.display_name = self.name
				the_email.owner.save()
		the_org, org_is_new = Organization.objects.get_or_create(name=self.organization)
		if self.account == None:
			self.account, a_is_new = Account.objects.get_or_create(owner=the_email.owner, managed=the_org)
		
		super(HelpRequest, self).save(*args, **kwargs)

