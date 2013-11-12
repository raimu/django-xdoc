from django.db import models
from django.forms import ModelForm
from xdoc.models import Node


class Picto(models.Model):
    label = models.CharField(max_length=100)
    path = models.CharField(max_length=100)

    def __unicode__(self):
        return self.label


class BusinessCard(Node):
    COLOR = (
        ('#ff0000', 'red'),
        ('#00ff00', 'green'),
        ('#0000ff', 'blue'),
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    color = models.CharField(max_length=7, choices=COLOR, blank=True)
    pictos = models.ManyToManyField(Picto, blank=True, null=True)


class BusinessCardForm(ModelForm):
    class Meta:
        model = BusinessCard