from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import TestAppView, edit_view


urlpatterns = patterns('',
	url(r"^$", TemplateView.as_view(template_name="base.html"), name="home"),
	url(r"^(?P<model_name>\w+)/(?P<pk>\d+)/", edit_view, name="dynamic_models_edit"),
	url(r"^(?P<model_name>\w+)/$", TestAppView.as_view(), name='dynamic_models'),
)
