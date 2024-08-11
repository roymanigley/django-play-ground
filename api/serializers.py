from rest_framework import serializers
from core.models import Movie, Actor, MovieActor, Customer, Country, Rental, Address


class MovieSerializer(serializers.ModelSerializer):

    class _MovieActorSerializer(serializers.ModelSerializer):
        class _ActorSerializer(serializers.ModelSerializer):

            class Meta:
                model = Actor
                fields = ['id', 'name']

        actor = _ActorSerializer(read_only=True)

        class Meta:
            model = MovieActor
            fields = ['actor', 'character']

    characters = _MovieActorSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ['id', 'name', 'characters', 'price_per_day']


class ActorSerializer(serializers.ModelSerializer):

    class _MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ['id', 'name', 'price_per_day']

    movies = _MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = '__all__'


class MovieActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieActor
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class _AddressSerializer(serializers.ModelSerializer):
        class _CountrySerializer(serializers.ModelSerializer):

            class Meta:
                model = Country
                fields = '__all__'

        country = _CountrySerializer()

        class Meta:
            model = Address
            fields = '__all__'

    delivery_address = _AddressSerializer(read_only=True)
    billing_address = _AddressSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'


class RentalSerializer(serializers.ModelSerializer):

    class _CustomerSerializer(serializers.ModelSerializer):

        class Meta:
            model = Customer
            fields = ['id', 'first_name', 'last_name']

    class _MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ['id', 'name', 'price_per_day']

    customer = _CustomerSerializer(read_only=True)
    movie = _MovieSerializer(read_only=True)

    def to_internal_value(self, data):
        instance = super().to_internal_value(data)
        customer_id = data.get('customer', {}).get('id')
        movie_id = data.get('movie', {}).get('id')

        if customer_id:
            instance.customer = Customer.objects.filter(id=customer_id).first()
        if movie_id:
            instance.movie = Movie.objects.filter(id=movie_id).first()

        return instance

    class Meta:
        model = Rental
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class _CountrySerializer(serializers.ModelSerializer):

        class Meta:
            model = Country
            fields = '__all__'

    country = _CountrySerializer(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
