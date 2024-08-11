from rest_framework.viewsets import ModelViewSet
from core.models import Movie, Actor, Customer, Address, Country, Rental
from .serializers import MovieSerializer, ActorSerializer, MovieActorSerializer, CustomerSerializer, AddressSerializer, CountrySerializer, RentalSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions


class MovieViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Movie.objects.prefetch_related('characters__actor').all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'characters__character': ['exact', 'icontains'],
        'characters__actor__name': ['exact', 'icontains'],
    }


class ActorViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Actor.objects.prefetch_related('characters__movie').all()
    serializer_class = ActorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'movies__name': ['exact', 'icontains'],
    }


class CustomerViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Customer.objects.select_related(
        'delivery_address__country'
    ).select_related(
        'billing_address__country'
    ).all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'first_name': ['exact', 'icontains'],
        'last_name': ['exact', 'icontains'],
    }


class AddressViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Address.objects.select_related('country').all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'address': ['exact', 'icontains'],
    }


class CountryViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'iso_a_3': ['exact', 'icontains'],
    }


class RentalViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Rental.objects.select_related(
        'customer'
    ).select_related(
        'movie'
    ).all()
    serializer_class = RentalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'customer__id': ['exact'],
        'movie__id': ['exact'],
        'date_to': ['exact', 'isnull'],
    }
