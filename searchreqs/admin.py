from django.contrib import admin

# Register your models here.
from .models import Searchreq

class SearchreqAdmin(admin.ModelAdmin):
	list_display = ['__unicode__','query','timestamp']
	class Meta:
		model = Searchreq

admin.site.register(Searchreq,SearchreqAdmin)

