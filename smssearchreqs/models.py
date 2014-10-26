from django.db import models

# Create your models here.
class smssearchreq(models.Model):
	 mobilenum=models.DecimalField(max_digits=10,decimal_places=0)
	 query = models.CharField(max_length=200)
	 timestamp=models.DateTimeField(auto_now_add=True)

	 def __unicode__(self):
	 	return "%s" %(self.mobilenum)
