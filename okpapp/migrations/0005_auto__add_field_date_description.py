# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Date.description'
        db.add_column(u'okpapp_date', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Date.description'
        db.delete_column(u'okpapp_date', 'description')


    models = {
        u'okpapp.application': {
            'Meta': {'object_name': 'Application'},
            'apply_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'charged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'facebook_url': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requests': ('django.db.models.fields.TextField', [], {}),
            'stripe_token': ('django.db.models.fields.TextField', [], {'max_length': '400'})
        },
        u'okpapp.date': {
            'Meta': {'object_name': 'Date'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_application'", 'to': u"orm['okpapp.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['okpapp.Location']", 'null': 'True'}),
            'second_application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_application'", 'to': u"orm['okpapp.Application']"})
        },
        u'okpapp.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['okpapp']