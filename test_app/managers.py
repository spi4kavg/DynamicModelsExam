from django.db import models
from django.core import serializers
import json


def field_to_type(field):
	type_name = None
	if isinstance(field, models.CharField):
		type_name = 'char'
	elif isinstance(field, models.IntegerField):
		type_name = 'int'
	elif isinstance(field, models.DateField):
		type_name = 'date'
	return type_name


class DynamicModelManager(models.Manager):
	def serialize(self, *args, **kwargs):
		queryset = self.all()
		serialized = {}
		
		serialized = {
			"model_header": [],
			"model_body": []
		}
		if queryset:
			serialized["model_header"] = [{
				"verbose_name": u"%s" % (field.verbose_name, ),
				"name": u"%s" % (field.name, ),
				"type": u"%s" % (field_to_type(field), ),
			} for field in queryset[0]._meta.fields]

			serialized["model_body"] = []
			for query in queryset:
				dictionary = {
					"pk": query.pk,
					"fields": []
				}
				for field in query._meta.fields:
					dictionary["fields"].append({
						"name": u"%s" % (field.name, ),
						"value": u"%s" % (getattr(query, field.attname), )
					})
				serialized["model_body"].append(dictionary)
		return serialized