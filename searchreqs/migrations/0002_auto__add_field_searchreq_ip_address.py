# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Searchreq.ip_address'
        db.add_column(u'searchreqs_searchreq', 'ip_address',
                      self.gf('django.db.models.fields.CharField')(default='ABC', max_length=120),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Searchreq.ip_address'
        db.delete_column(u'searchreqs_searchreq', 'ip_address')


    models = {
        u'searchreqs.searchreq': {
            'Meta': {'object_name': 'Searchreq'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'default': "'ABC'", 'max_length': '120'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['searchreqs']