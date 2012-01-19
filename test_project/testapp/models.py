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
        return "%s x %s x %s" % (self.height, self.width, self.max_pages)


class Factory(models.Model):
    address = models.CharField(max_length=255)
    book_formats = models.ManyToManyField(BookFormat, blank=True, null=True)

    def __unicode__(self):
        return "address: %s with formats %s" % (
                self.address,
                ",".join([str(bf) for bf in self.book_formats.all()]),
        )






class Animal(models.Model):
    more_info = models.TextField()
    image = models.ImageField(max_length=255, upload_to="animal_pictures")

    def __unicode__(self):
        return "more_info: %s" % self.more_info

class Farm(models.Model):
    name = models.CharField(max_length=255)
    ducks = models.ManyToManyField(Animal, blank=True, null=True, related_name="duck_set")
    chickens = models.ManyToManyField(Animal, blank=True, null=True, related_name="chicken_set")

    def __unicode__(self):
        return "name: %s, with %d ducks and %d chickens" % (
                self.name,
                self.ducks.all().count(),
                self.chickens.all().count()
        )
