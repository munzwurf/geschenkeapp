from __future__ import unicode_literals
from django.db import models
import datetime



class AttributeType(models.Model):
	attribute_type_name = models.CharField(max_length = 999)
	question_text = models.CharField(max_length = 999)
	select = models.IntegerField(default = 1)
        
	def __str__(self):
		return self.attribute_type_name

class Attribute(models.Model):
	attribute_name = models.CharField(max_length = 999)
	attribute_type = models.ForeignKey(AttributeType, on_delete=models.CASCADE)
    
	def __str__(self):
		return self.attribute_name

class Gifts(models.Model):
    name = models.CharField(max_length = 999)
    price = models.DecimalField(max_digits = 5,decimal_places=2, default = 1.00)
    url = models.URLField(default = "http")
    img_url = models.URLField(default = "http")
    prim_attr = models.ManyToManyField(Attribute, related_name = "prim_attr")
    sec_attr = models.ManyToManyField(Attribute, related_name = "sec_attr")

    def __str__(self):
    	return self.name