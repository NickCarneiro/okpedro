# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table(u'okpapp_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('facebook_url', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('requests', self.gf('django.db.models.fields.TextField')()),
            ('apply_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('stripe_token', self.gf('django.db.models.fields.TextField')(max_length=400)),
        ))
        db.send_create_signal(u'okpapp', ['Application'])


    def backwards(self, orm):
        # Deleting model 'Application'
        db.delete_table(u'okpapp_application')


    models = {
        u'okpapp.application': {
            'Meta': {'object_name': 'Application'},
            'apply_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'facebook_url': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requests': ('django.db.models.fields.TextField', [], {}),
            'stripe_token': ('django.db.models.fields.TextField', [], {'max_length': '400'})
        }
    }

    complete_apps = ['okpapp']