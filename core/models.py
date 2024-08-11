from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=255)
    price_per_day = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Actor(models.Model):
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(
        'Movie', related_name='actor', through='MovieActor', db_index=True
    )

    def __str__(self):
        return self.name


class MovieActor(models.Model):
    character = models.CharField(max_length=255)
    actor = models.ForeignKey(
        'Actor', on_delete=models.DO_NOTHING, related_name='characters', db_index=True
    )
    movie = models.ForeignKey(
        'Movie', on_delete=models.DO_NOTHING, related_name='characters', db_index=True
    )

    def __str__(self):
        return f'{self.actor.name} ({self.actor.name})'


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    delivery_address = models.ForeignKey(
        'Address', on_delete=models.CASCADE, related_name='delivery_addresses', db_index=True
    )
    billing_address = models.ForeignKey(
        'Address', on_delete=models.CASCADE, related_name='billing_addresses', db_index=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Address(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    zip = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.ForeignKey(
        'Country', on_delete=models.DO_NOTHING, related_name='countries', db_index=True
    )

    def __str__(self):
        return f'{self.name} {self.address}, {self.zip} {self.city}, {self.country.name}'


class Country(models.Model):
    name = models.CharField(max_length=255)
    iso_a_3 = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.name} ({self.iso_a_3})'


class Rental(models.Model):
    date_from = models.DateField()
    date_to = models.DateField(null=True)
    remark = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(
        'Customer', on_delete=models.DO_NOTHING, related_name='customers', db_index=True
    )
    movie = models.ForeignKey(
        'Movie', on_delete=models.DO_NOTHING, related_name='movies', db_index=True
    )

    def __str__(self):
        return f'{self.movie.name}: {self.customer.first_name} {self.customer.last_name} ({self.date_from} - {self.date_to})'
