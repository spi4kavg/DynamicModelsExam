from django.db import models
import yaml
from settings import CONFIG_FILE, DEFAULT_CHAR_LEN, DEFAULT_INT_VAL
from .managers import DynamicModelManager


class DynamicModelConstructor(object):
	models = {}
	cfg = {}

	def __contains__(self, model_name):
		return model_name in self.__class__.models

	def __iter__(self):
		for model in self.models.values():
			yield model

	def contribute_to_class(self, cls, name):
		models.signals.class_prepared.connect(self.prepared, sender=cls)

	def prepared(self, *args, **kwargs):
		stream = open(CONFIG_FILE, "r")
		cfg = yaml.load(stream)
		for model_name, model_cfg in cfg.items():
			dmodel = self.create(model_name, model_cfg)

	def create(self, model_name, model_cfg):
		attrs = self.get_fields(model_cfg)
		attrs.update(Meta=type('Meta', (), {
			'verbose_name': u'%s' % model_cfg.get('title'),
			'verbose_name_plural': u'%s' % model_cfg.get('title')
		}))
		self.models[model_name] = type(model_name, (models.Model,), attrs)

	def get_fields(self, model_cfg):
		fields = {
			'id': models.AutoField(primary_key=True),
			'__module__': self.__module__,
			'__unicode__': lambda self: u'%s' % model_cfg.get("title"),
			'objects': DynamicModelManager(),
		}
		for field in model_cfg.get('fields', {}):
			fields.update(self.field_name_to_object(field))
		return fields

	def field_name_to_object(self, field_cfg):
		field = None
		if field_cfg.get('type') == 'char':
			field = models.CharField(max_length=DEFAULT_CHAR_LEN,
				verbose_name=field_cfg.get('title'))
		elif field_cfg.get("type") == 'int':
			field = models.IntegerField(default=DEFAULT_INT_VAL,
				verbose_name=field_cfg.get('title'))
		elif field_cfg.get('type') == 'date':
			field = models.DateField(verbose_name=field_cfg.get("title"))
		return {field_cfg.get("id"): field}


class DynamicModel(models.Model):
	models = DynamicModelConstructor()