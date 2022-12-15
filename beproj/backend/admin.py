from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Policy)
admin.site.register(Element)
admin.site.register(Edit)
admin.site.register(Profile)
admin.site.register(ElementFlag)