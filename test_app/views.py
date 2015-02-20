# -*- coding: utf8 -*-
from django.shortcuts import render
from django.db.models import get_model
from django.http import Http404, HttpResponse
from django.views.generic import View
import json
from django.views.decorators.http import require_http_methods


class TestAppView(View):
	def get(self, request, model_name):
		try:
			model = get_model('test_app', model_name)
		except LookupError:
			raise Http404
		qs = model.objects.serialize()
		return HttpResponse(json.dumps(qs))


	def post(self, request, model_name):
		response = {
			"errors": []
		}
		try:
			model = get_model('test_app', model_name)
			model(**request.POST.dict()).save()
		except LookupError:
			raise Http404
		return HttpResponse(json.dumps(response))


@require_http_methods(["POST"])
def edit_view(request, model_name, pk):
	response = {
		"errors": []
	}
	try:
		model = get_model('test_app', model_name)
		obj = model.objects.filter(pk=pk)\
			.update(**request.POST.dict())
	except LookupError:
		raise Http404
	return HttpResponse(json.dumps(response))