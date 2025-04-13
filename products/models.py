import uuid
from django.db import models

# Create your models here.


class Category(models.Model):
    """
    Model representing categories (e.g. Tea, Kit, Equipment)
    """

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
    """
    Model representing country of origin (e.g. Japan, China)
    """
    class Meta:
        verbose_name_plural = 'Countries'
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=75)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.country


class Tea(models.Model):
    """
    Model representing tea products
    Tea has unique fields of blend, weight and country of origin
    """
    class Meta:
        verbose_name_plural = 'Tea'
        db_table = 'products_tea'

    # Using UUID as a unique identifier across all models
    product_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
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
    """
    Model representing equipment products
    Equipment has unique fields of country of origin
    """
    class Meta:
        verbose_name_plural = 'Equipment'

    # Using UUID as a unique identifier across all models
    product_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
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
    """
    Model representing kit products
    kit does not have unique fields
    """
    # Using UUID as a unique identifier across all models
    product_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    internal_name = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.internal_name
