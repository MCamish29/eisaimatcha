import uuid
from django.db import models

# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.category 
    
    def get_friendly_name(self):
        return self.category


class Country(models.Model):
    class Meta:
        verbose_name_plural = 'Countries'
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=75)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.country


class Tea(models.Model):
    class Meta:
        verbose_name_plural = 'Tea'
        db_table = 'products_tea'
    
    # Using UUID as a unique identifier across all models
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    internal_name = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField()
    blend = models.CharField(max_length=250, null=True, blank=True)
    weight = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.internal_name


class Equipment(models.Model):
    class Meta:
        verbose_name_plural = 'Equipment'
    
    # Using UUID as a unique identifier across all models
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    internal_name = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.internal_name


class Kit(models.Model):
    # Using UUID as a unique identifier across all models
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    internal_name = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='media/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.internal_name
