#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','geschenke.settings')

import django
django.setup()
from main.models import Attribute, AttributeType, Gifts

import csv


def populate():
	attribute_types = [
		["gender", "What is the gender?"],
		["age", "What is the age?"],
		["relationship", "What is your relationship?"],
		["occasion", "What is the occasion?"],
		["interests", "What is their interest?"],
		 ]
	
	attributes = {
		"gender":["male","female"],
		"age":["0-9","10-19","20-39","40-99"],
		"relationship":["Partner","Friend","Parent","Colleague","Child"],
		"occasion":["Birthday","Christmas","No occasion"],
		"interests":["Electronics","Animals","Travel","Gardening","Sports","Fashion","Food","Wellness","Party"]}

	gift_list = []
	with open ('geschenke.csv') as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		for row in reader:
			gift_list.append(row)

	
	for a in attribute_types:
		p = AttributeType.objects.get_or_create(attribute_type_name = a[0], question_text = a[1])[0]
		p.save()
		print("Added: {0}".format(p.attribute_type_name))
	
	for key,value in attributes.iteritems():
		atttype = AttributeType.objects.get(attribute_type_name=key)
		for e in value:
			p = Attribute.objects.get_or_create(attribute_name = e, attribute_type=atttype)[0]
			p.save()
		print("Added: {0} - {1}".format(p.attribute_type, p.attribute_name))

 	for g in gift_list:
		p = Gifts.objects.get_or_create(name = g[1], 
										price = g[2],
										img_url = g[3],
										url = g[4],)[0]
		p.save()
		prim_attr_list = g[10].split(";")
		sec_attr_list = g[11].split(";")
		for a in prim_attr_list:
			attr = Attribute.objects.get(attribute_name=a)
			p.prim_attr.add(attr)
		for a in sec_attr_list:
			attr = Attribute.objects.get(attribute_name=a)
			p.sec_attr.add(attr)
		print "Added: "+ p.name


# Start execution here!
if __name__ == '__main__':
	print("Starting population script...")
	populate()