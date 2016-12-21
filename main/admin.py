from django.contrib import admin
from .models import Attribute, AttributeType, Gifts

admin.site.register(AttributeType)
admin.site.register(Attribute)
admin.site.register(Gifts)