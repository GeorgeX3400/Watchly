from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)  
    has_premium = models.BooleanField(default=False)
    cod = models.CharField(max_length=100, null=True, blank=True, unique=True)
    email_confirmat = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)



    def __str__(self):
        return self.name

class MovementType(models.Model):
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.type

class Warranty(models.Model):
    duration_years = models.IntegerField()
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.duration_years} years"

class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Watch(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    water_resistance = models.IntegerField()  
    description = models.TextField(blank=True, null=True)
    movement_type = models.ForeignKey(MovementType, on_delete=models.SET_NULL, null=True)
    warranty = models.ForeignKey(Warranty, on_delete=models.SET_NULL, null=True)
    materials = models.ManyToManyField(Material, through='WatchMaterial')
    features = models.ManyToManyField(Feature, through='WatchFeature')
    updatedAt = models.DateField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("vizualizeaza_oferta", "Poate vizualiza oferta")
        ]

class WatchMaterial(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watch.name} - {self.material.name}"

class WatchFeature(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watch.name} - {self.feature.name}"

class Stock(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.watch.name} - {self.location}: {self.quantity} pcs"


class Visualization(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    watch = models.ForeignKey('Watch', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']  
 
class Promotion(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    categories = models.ManyToManyField(Feature)  

    def __str__(self):
        return self.name

def add_visualization(user, watch, N=5):
    Visualization.objects.create(user=user, watch=watch)
    visualizations = Visualization.objects.filter(user=user).order_by('-viewed_at')
    if visualizations.count() > N:
        visualizations.last().delete()

class FailedLoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)


# ORDERS:

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey('Watch', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"




    
        