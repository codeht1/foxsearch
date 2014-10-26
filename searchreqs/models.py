from django.db import models

# Create your models here.
class Searchreq(models.Model):
	 email = models.EmailField()
	 ip_address = models.CharField(max_length=120,default='ABC')
	 query = models.CharField(max_length=200)
	 timestamp=models.DateTimeField(auto_now_add=True)

	 def __unicode__(self):
	 	return "%s" %(self.email)
