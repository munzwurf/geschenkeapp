#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.views import generic
from main.models import Attribute, AttributeType, Gifts
import operator




questions = AttributeType.objects.all()
gifts = Gifts.objects.all()
submitted_attributes = {}
question_list = []
answered_questions = []

def index(request):
	global question_list, answered_questions
	question_list = list(questions)
	answered_questions = []

	question = question_list[0]
	answered_questions.append(question_list[0])
	question_list.pop(0)
	return render (request, 'main/index.html', {'question' : question},)

def results(request):
	try:
		
#		best_gifts = find_best_gifts(request.POST,3)
		best_gifts = find_best_gifts(submitted_attributes,3)
		#print best_gifts
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
	global question_list, answered_questions
	back = 1
	last = 0
	attribute = request.GET.get('val_chosen', None)
	attribute_type = request.GET.get('att_type', None)
	input_type = request.GET.get('input_type', None)
	print question_list
	if question_list == []:
		last = 1
		data = {'last':last,'back':back}

	else:
		if input_type == "radio":
			submitted_attributes[attribute_type] = attribute
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
		'last':last,
		'back':back
		}
	#print submitted_attributes
	return	JsonResponse(data)