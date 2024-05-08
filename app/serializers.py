from .models import Category, Brand, Model, Stock, Booking
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'category', 'title']

class StockSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='model.category.title', read_only=True)
    model_id = serializers.IntegerField(source='model.id', read_only=True)
    model_title = serializers.CharField(source='model.title', read_only=True)
    brand_title = serializers.CharField(source='model.brand.title', read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'model_id', 'category_title', 'brand_title', 'model_title']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'stock', 'start_date', 'end_date']
        read_only_fields = ['user']

    def validate_start_date(self, value):
        if value <= timezone.now() + timezone.timedelta(hours=1):
            raise serializers.ValidationError("Start date must be at least one hour from now.")
        if value.minute != 0 or value.second != 0:
            raise serializers.ValidationError("Start date must have 0 minutes and seconds.")
        return value

    def validate_end_date(self, value):
        start_date = datetime.strptime(self.initial_data.get('start_date'), "%Y-%m-%dT%H:%M")
        if value <= start_date:
            raise serializers.ValidationError("End date must be after start date.")
        if value.minute != 0 or value.second != 0:
            raise serializers.ValidationError("End date must have 0 minutes and seconds.")
        if (value - start_date) < timezone.timedelta(hours=4):
            raise serializers.ValidationError("The duration between start date and end date must be at least 4 hours.")
        return value
        return value

    def validate_stock(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Selected stock is not active.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        data['user'] = user
        if 'status' in data:
            raise serializers.ValidationError("Status cannot be set directly.")
        return data

    def update(self, instance, validated_data):
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance