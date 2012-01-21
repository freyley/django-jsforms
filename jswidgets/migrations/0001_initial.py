# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TemporaryUploadedImage'
        db.create_table('jswidgets_temporaryuploadedimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timage', self.gf('django.db.models.fields.files.ImageField')(max_length=500)),
        ))
        db.send_create_signal('jswidgets', ['TemporaryUploadedImage'])


    def backwards(self, orm):
        
        # Deleting model 'TemporaryUploadedImage'
        db.delete_table('jswidgets_temporaryuploadedimage')


    models = {
        'jswidgets.temporaryuploadedimage': {
            'Meta': {'object_name': 'TemporaryUploadedImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timage': ('django.db.models.fields.files.ImageField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['jswidgets']
