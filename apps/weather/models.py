from django.db import models


class Measurement(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2

    date = models.DateField(

    )
    variable = models.ForeignKey(
        'Variable',
        related_name='value_set'
    )
    station = models.ForeignKey(
        'Station',
        related_name='value_set'
    )
    value = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
    )
    status = models.SmallIntegerField(
        editable=False,
        default=STATUS_INACTIVE
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'weather'

    def __unicode__(self):
        return str(self.variable) + ' ' + str(self.value)


class Variable(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2

    code = models.CharField(max_length=10)
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    status = models.SmallIntegerField(
        editable=False,
        default=STATUS_INACTIVE
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'weather'

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)


class Station(models.Model):

    code = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    region = models.ForeignKey(
        'Region',
        related_name='station_set'
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'weather'

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)


class Region(models.Model):

    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'weather'

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)


class Filter(models.Model):

    value = models.CharField(
        max_length=10,
        blank=True,
        unique=True
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'weather'

    def __unicode__(self):
        return self.value
