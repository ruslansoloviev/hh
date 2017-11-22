
from django.db import models


def _get_class_vars(cls):
    v = filter(lambda x: not x.startswith('_'), vars(cls))
    return str(dict(map(lambda k: (k, cls.__dict__[k]), v)))


class Metro(models.Model):
    station_id = models.CharField(max_length=6, primary_key=True)
    station_name = models.CharField(max_length=30, verbose_name='Станция метро')
    line_id = models.CharField(max_length=2)
    line_name = models.CharField(max_length=30, verbose_name='Ветка метро')
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return _get_class_vars(self)

    def __unicode__(self):
        return self.__str__()


class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=20, null=True, verbose_name='Город')
    street = models.CharField(max_length=100, null=True, verbose_name='Улица')
    building = models.CharField(max_length=10, null=True, verbose_name='Дом')
    description = models.CharField(max_length=100, null=True, verbose_name='Комментарий')
    raw = models.CharField(max_length=100, null=True, verbose_name='Оригинал строки адреса')
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    metro_stations = models.ManyToManyField(Metro, verbose_name='Станции метро')

    def __str__(self):
        return _get_class_vars(self)

    def __unicode__(self):
        return self.__str__()
