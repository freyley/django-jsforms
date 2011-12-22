from django.db import models

# Create your models here.
class Foo(models.Model):
    name = models.CharField(max_length=255)
    foodate = models.DateField()

    def __unicode__(self):
        return self.name

class Baz(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Bar(models.Model):
    name = models.CharField(max_length=255)
    foo = models.ForeignKey(Foo)
    bazes = models.ManyToManyField(Baz, blank=True, null=True)

    def __unicode__(self):
        n = self.name
        n += " with foo: " % self.foo
        n += " and %d bazes," % self.bazes.all().count()
        n += ",".join(self.bazes.all())
        return n


