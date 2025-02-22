from rest_framework import serializers
from .models import *
from datetime import date
from django.core.exceptions import ValidationError


# MODELS SERIALIZERS: 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address', 'bio', 'has_premium']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country']

class MovementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementType
        fields = ['id', 'type', 'description']

class WarrantySerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranty
        fields = ['id', 'duration_years', 'details']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'description']

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name', 'description']

class WatchMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchMaterial
        fields = ['watch', 'material']

class WatchFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchFeature
        fields = ['watch', 'feature']

class WatchSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    movement_type = MovementTypeSerializer(read_only=True)
    warranty = WarrantySerializer(read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Watch
        fields = ['id', 'name', 'brand', 'price', 'water_resistance', 'description', 'movement_type', 'warranty', 'materials', 'features']



class VisualizationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # Nested CustomUserSerializer for user data
    watch = WatchSerializer(read_only=True)  # Nested WatchSerializer for watch data

    class Meta:
        model = Visualization
        fields = ['id', 'user', 'watch', 'viewed_at']


class PromotionSerializer(serializers.ModelSerializer):
    categories = FeatureSerializer(many=True, read_only=True)  # Nested FeatureSerializer for related data

    class Meta:
        model = Promotion
        fields = ['id', 'name', 'created_at', 'expires_at', 'subject', 'message', 'categories']


class OrderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # Nested CustomUserSerializer for user data

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price']


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)  # Nested OrderSerializer for order data
    product = WatchSerializer(read_only=True)  # Nested WatchSerializer for product (watch) data

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']


#FORM SERIALIZERS:

class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)
    surname = serializers.CharField(required=False)
    birthdate = serializers.DateField()
    email = serializers.EmailField()
    confirm_email = serializers.EmailField()
    message_type = serializers.ChoiceField(
        choices=[
            ('reclamatie', 'Complaint'),
            ('intrebare', 'Question'),
            ('review', 'Review'),
            ('cerere', 'Request'),
            ('programare', 'Appointment')
        ]
    )
    subject = serializers.CharField()
    min_wait_days = serializers.IntegerField(min_value=1)
    message = serializers.CharField()

    def validate_birthdate(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("You must be at least 18 years old.")
        return value

    def validate(self, data):
        # Check if emails match

        
        if data.get("email") != data.get("confirm_email"):
            raise serializers.ValidationError({"confirm_email": "Emails do not match."})

        # Validate message field
        message = data.get("message")
        if message:
            word_count = len(message.split())
            if word_count < 5 or word_count > 100:
                raise serializers.ValidationError({"message": "Message must contain between 5 and 100 words."})
            if "http://" in message or "https://" in message:
                raise serializers.ValidationError({"message": "Message cannot contain links."})
            if not message.strip().endswith(data.get("name")):
                raise serializers.ValidationError({"message": "Message must end with your name as a signature."})

        return data

