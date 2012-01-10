from django.contrib import admin
from models import Author, Book, BookFormat, Publisher, Factory

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookFormat)
admin.site.register(Publisher)
admin.site.register(Factory)

