from app.models import ModelInput, ModelOutput
from django.contrib import admin
from .models import *

admin.site.register(ModelInput)
admin.site.register(ModelOutput)