from rest_framework import serializers
from .models import Listings, Booking, Review
from django.contrib.auth.models import User

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listings
        fields = '__all__'
        read_only_fields = ('listing_id','created_at', 'updated_at')

    def create(self, validated_data):
        return Listings.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.price_per_night = validated_data.get('price_per_night', instance.price_per_night)
        instance.save()
        return instance


class BookingSerializer(serializers.ModelSerializer):
    listing_id = serializers.PrimaryKeyRelatedField(queryset=Listings.objects.all(),
                                                    source='listing',
                                                    write_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('booking_id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        return Listings.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.listing = validated_data.get('listing', instance.listing)
        instance.guest = validated_data.get('guest', instance.guest)
        instance.status = validated_data.get('status', instance.status)
        instance.check_in = validated_data.get('check_in', instance.check_in)
        instance.check_out = validated_data.get('check_out', instance.check_out)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    listing_id = serializers.PrimaryKeyRelatedField(queryset=Listings.objects.all(),
                                                    source='listing',
                                                    write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                 source='guest',
                                                 write_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('review_id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        return Review.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.listing = validated_data.get('listing', instance.listing)
        instance.guest = validated_data.get('guest', instance.guest)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance