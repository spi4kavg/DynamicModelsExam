from django.contrib import admin
from .models import DynamicModelConstructor


dModels = DynamicModelConstructor()

admin.site.register([model for model in dModels])