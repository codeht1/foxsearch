# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'smssearchreq'
        db.create_table(u'smssearchreqs_smssearchreq', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mobilenum', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=0)),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'smssearchreqs', ['smssearchreq'])


    def backwards(self, orm):
        # Deleting model 'smssearchreq'
        db.delete_table(u'smssearchreqs_smssearchreq')


    models = {
        u'smssearchreqs.smssearchreq': {
            'Meta': {'object_name': 'smssearchreq'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobilenum': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '0'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['smssearchreqs']