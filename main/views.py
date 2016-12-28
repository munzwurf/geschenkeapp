#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.views import generic
from main.models import Attribute, AttributeType, Gifts
import operator
import json




questions = AttributeType.objects.all()
gifts = Gifts.objects.all()
submitted_attributes = {}
question_list = []
answered_questions = []

def index(request):
	global question_list, answered_questions, submitted_attributes
	question_list = list(questions)
	answered_questions = []
	submitted_attributes = {}
	print submitted_attributes
	question = question_list[0]
	answered_questions.append(question_list[0])
	question_list.pop(0)
	return render (request, 'main/index.html', {'question' : question},)

def results(request):
	
	try:
		print submitted_attributes

		best_gifts = find_best_gifts(submitted_attributes,3)
		return render (request, 'main/result.html', {'best_gifts':best_gifts})
	except (KeyError):
		return render (request, 'main/index.html', {'questions' : questions, 
													'error_message':"Please select all choices."})

def find_best_gifts(attr,lim):
	gender = attr['gender']
	attr_val = attr.values()
	attr_val.remove(gender)

	# Step 1: Filter for primary attributes
	g1 = Gifts.objects.filter(prim_attr__attribute_name = gender)
	g2 = Gifts.objects.filter(prim_attr__attribute_name__in = attr_val)
	gift_list  = list(set(g1) & set(g2))
	#print gift_list

	# Step 2: Find gifts with most secondary attributes

	for gift in gift_list:
		gift_object = Gifts.objects.get(name = gift)
		gift_sec_attr = gift_object.sec_attr.all()
		intersect = set(gift_sec_attr).intersection(attr_val)
		# Build dictionary of Gift : no. of intersections and then get maximum X values to display
	#return gift_list
	return list(gifts)

def next_question(request):
	global question_list, answered_questions, submitted_attributes
	back = 1

	attribute = request.GET.get('val_chosen', None)
	if attribute:
		attribute = json.loads(attribute)
	attribute_type = request.GET.get('att_type', None)
	input_type = request.GET.get('input_type', None)

	
	if input_type == "choice":
		submitted_attributes[attribute_type] = attribute
		if question_list == []:
			result = reverse('main:results')
			data = {'result':result}
			return JsonResponse(data)
		else:
			question = question_list[0]
			answered_questions.append(question_list[0])
			question_list.pop(0)
			attribute_names = question.attribute_set.all().values('attribute_name')
	else:
		question = answered_questions[-2]
		question_list.insert(0,answered_questions[-1])
		answered_questions.pop()
		attribute_names = question.attribute_set.all().values('attribute_name')

	if len(answered_questions) in [0,1]:
		back = 0
	

	data = {
	'question_text':question.question_text,
	'attribute_type_name':question.attribute_type_name,
	'attribute_names':list(attribute_names),
	'back':back,
	'select':question.select}
	print submitted_attributes
	return	JsonResponse(data)