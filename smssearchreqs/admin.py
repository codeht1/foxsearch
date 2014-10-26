from django.contrib import admin

# Register your models here.
from .models import smssearchreq

class smssearchreqAdmin(admin.ModelAdmin):
	list_display = ['__unicode__','query','timestamp']
	class Meta:
		model = smssearchreq

admin.site.register(smssearchreq,smssearchreqAdmin)

