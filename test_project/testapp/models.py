from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher)
    books = models.ManyToManyField(Book, blank=True, null=True)

    def __unicode__(self):
        n = self.name
        n += " has publisher : " + str(self.publisher)
        n += " and %d books," % self.books.all().count()
        n += ",".join([str(book) for book in self.books.all()])
        return n


class BookFormat(models.Model):
    height = models.CharField(max_length=255)
    width = models.CharField(max_length=255)
    max_pages = models.IntegerField(max_length=255)

    def __unicode__(self):
        return self.thing_one


class Factory(models.Model):
    address = models.CharField(max_length=255)
    book_formats = models.ManyToManyField(BookFormat, blank=True, null=True)
