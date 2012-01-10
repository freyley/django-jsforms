# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Publisher'
        db.create_table('testapp_publisher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('testapp', ['Publisher'])

        # Adding model 'Book'
        db.create_table('testapp_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('testapp', ['Book'])

        # Adding model 'Author'
        db.create_table('testapp_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testapp.Publisher'])),
        ))
        db.send_create_signal('testapp', ['Author'])

        # Adding M2M table for field books on 'Author'
        db.create_table('testapp_author_books', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('author', models.ForeignKey(orm['testapp.author'], null=False)),
            ('book', models.ForeignKey(orm['testapp.book'], null=False))
        ))
        db.create_unique('testapp_author_books', ['author_id', 'book_id'])

        # Adding model 'BookFormat'
        db.create_table('testapp_bookformat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('max_pages', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
        ))
        db.send_create_signal('testapp', ['BookFormat'])

        # Adding model 'Factory'
        db.create_table('testapp_factory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('testapp', ['Factory'])

        # Adding M2M table for field book_formats on 'Factory'
        db.create_table('testapp_factory_book_formats', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factory', models.ForeignKey(orm['testapp.factory'], null=False)),
            ('bookformat', models.ForeignKey(orm['testapp.bookformat'], null=False))
        ))
        db.create_unique('testapp_factory_book_formats', ['factory_id', 'bookformat_id'])


    def backwards(self, orm):
        
        # Deleting model 'Publisher'
        db.delete_table('testapp_publisher')

        # Deleting model 'Book'
        db.delete_table('testapp_book')

        # Deleting model 'Author'
        db.delete_table('testapp_author')

        # Removing M2M table for field books on 'Author'
        db.delete_table('testapp_author_books')

        # Deleting model 'BookFormat'
        db.delete_table('testapp_bookformat')

        # Deleting model 'Factory'
        db.delete_table('testapp_factory')

        # Removing M2M table for field book_formats on 'Factory'
        db.delete_table('testapp_factory_book_formats')


    models = {
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
        'testapp.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['testapp']
