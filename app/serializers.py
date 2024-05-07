from django.contrib.auth.models import User
from .models import Category, Brand, Model, Stock, Order
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    password = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('User already exists')
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('User already exists')
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
    

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Category` instance, given the validated data.
        """
        if Category.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError('Category already exists')
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Category` instance, given the validated data.
        """
        if Category.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError('Category already exists')
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class BrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Brand` instance, given the validated data.
        """
        if Brand.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError('Brand already exists')
        return Brand.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Brand` instance, given the validated data.
        """
        if Brand.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError('Brand already exists')
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
    
class ModelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    title = serializers.CharField(max_length=100)
    weight = serializers.DecimalField(max_digits=10, decimal_places=2)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        """
        Create and return a new `Model` instance, given the validated data.
        """
        if Model.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError('Model already exists')
        return Model.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Model` instance, given the validated data.
        """
        if Model.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError('Model already exists')
        instance.category = validated_data.get('category', instance.category)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.title = validated_data.get('title', instance.title)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
    
class StockSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())
    is_active = serializers.BooleanField()

    def create(self, validated_data):
        """
        Create and return a new `Stock` instance, given the validated data.
        """
        if Stock.objects.filter(model=validated_data['model']).exists():
            raise serializers.ValidationError('Stock already exists')
        return Stock.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Stock` instance, given the validated data.
        """
        if Stock.objects.filter(model=validated_data['model']).exists():
            raise serializers.ValidationError('Stock already exists')
        instance.model = validated_data.get('model', instance.model)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    
class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all())
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=Order.STATUS)
    is_paid = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Order` instance, given the validated data.
        """
        return Order.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update for an existing `Order` instance, given the validated data for end_date, status and is_paid.
        """
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.status = validated_data.get('status', instance.status)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.save()
        return instance