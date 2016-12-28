#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','geschenke.settings')

import django
django.setup()
from main.models import Attribute, AttributeType, Gifts

import csv


def populate():
	attribute_list = []
	gift_list = []

	with open('attribute.csv') as attr_file:
		reader = csv.reader(attr_file)
		reader.next()
		for row in reader:
			attribute_list.append(row)

	with open ('geschenke.csv') as gift_file:
		reader = csv.reader(gift_file)
		reader.next()
		for row in reader:
			gift_list.append(row)

	
	for a in attribute_list:
		attr_type = AttributeType.objects.get_or_create(attribute_type_name = a[1], 
				question_text = a[2], select = a[3])[0]
		
		attr_type.save()
		print("Added: {0}".format(attr_type.attribute_type_name))

		attr_opt_list = a[4].split(";")
		for a_opt in attr_opt_list:
			attr_opt = Attribute.objects.get_or_create(attribute_name = a_opt,
												 attribute_type=attr_type)[0] 
			attr_opt.save()
			print("Added: " + attr_opt.attribute_name)
		

 	for g in gift_list:
		p = Gifts.objects.get_or_create(name = g[1], 
										price = g[2],
										img_url = g[3],
										url = g[4],)
		if p[1] == False:
			print "Already exists: " + p[0].name
		else:
			p = p[0]		
			p.save()
			prim_attr_list = g[5].split(";")
			sec_attr_list = g[6].split(";")
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