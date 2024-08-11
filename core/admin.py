from django.contrib import admin
from .models import Movie, Actor, MovieActor, Customer, Country, Address, Rental


admin.site.register(Actor)
admin.site.register(Address)
admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(Movie)
admin.site.register(MovieActor)
admin.site.register(Rental)
