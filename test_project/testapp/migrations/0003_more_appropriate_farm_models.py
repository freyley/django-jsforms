# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Farm.image'
        db.add_column('testapp_farm', 'image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=255), keep_default=False)

        # Removing M2M table for field chickens on 'Farm'
        db.delete_table('testapp_farm_chickens')

        # Removing M2M table for field ducks on 'Farm'
        db.delete_table('testapp_farm_ducks')

        # Adding M2M table for field animals on 'Farm'
        db.create_table('testapp_farm_animals', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farm', models.ForeignKey(orm['testapp.farm'], null=False)),
            ('animal', models.ForeignKey(orm['testapp.animal'], null=False))
        ))
        db.create_unique('testapp_farm_animals', ['farm_id', 'animal_id'])


    def backwards(self, orm):
        
        # Deleting field 'Farm.image'
        db.delete_column('testapp_farm', 'image')

        # Adding M2M table for field chickens on 'Farm'
        db.create_table('testapp_farm_chickens', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farm', models.ForeignKey(orm['testapp.farm'], null=False)),
            ('animal', models.ForeignKey(orm['testapp.animal'], null=False))
        ))
        db.create_unique('testapp_farm_chickens', ['farm_id', 'animal_id'])

        # Adding M2M table for field ducks on 'Farm'
        db.create_table('testapp_farm_ducks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farm', models.ForeignKey(orm['testapp.farm'], null=False)),
            ('animal', models.ForeignKey(orm['testapp.animal'], null=False))
        ))
        db.create_unique('testapp_farm_ducks', ['farm_id', 'animal_id'])

        # Removing M2M table for field animals on 'Farm'
        db.delete_table('testapp_farm_animals')


    models = {
        'testapp.animal': {
            'Meta': {'object_name': 'Animal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'more_info': ('django.db.models.fields.TextField', [], {})
        },
        'testapp.author': {
            'Meta': {'object_name': 'Author'},
            'books': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['testapp.Book']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testapp.Publisher']"})
        },
        'testapp.book': {
            'Meta': {'object_name': 'Book'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'testapp.bookformat': {
            'Meta': {'object_name': 'BookFormat'},
            'height': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_pages': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'testapp.factory': {
            'Meta': {'object_name': 'Factory'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'book_formats': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['testapp.BookFormat']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'testapp.farm': {
            'Meta': {'object_name': 'Farm'},
            'animals': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['testapp.Animal']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'testapp.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['testapp']
