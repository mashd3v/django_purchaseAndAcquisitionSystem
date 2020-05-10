from django.db import models
from bases.models import ModelClass

# Create your models here.
class Category(ModelClass):
    description = models.CharField(
        max_length=100,
        help_text='Description',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.description)
    
    def save(self):
        self.description = self.description.upper()
        super(Category, self).save()

    class Meta:
        verbose_name_plural = "Categories"

class Subcategory(ModelClass):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(
        max_length=100,
        help_text='Category Description'
    )

    def __str__(self):
        return '{}:{}'.format(self.category.description, self.description)

    def save(self):
        self.description = self.description.upper()
        super(Subcategory, self).save()

    class Meta:
        verbose_name_plural = "Subcategories"
        unique_together = ('category', 'description')

class Brand(ModelClass):
    description = models.CharField(
        max_length=100,
        help_text="Brand Description",
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.description)

    def save(self):
        self.description = self.description.upper()
        super(Brand, self).save()

    class Meta:
        verbose_name_plural = "Brands"

class MeasurementUnits(ModelClass):
    description = models.CharField(
        max_length=100,
        help_text="Brand Description",
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.description)

    def save(self):
        self.description = self.description.upper()
        super(MeasurementUnits, self).save()

    class Meta:
        verbose_name_plural = "Measurement Units"

class Product(ModelClass):
    code = models.CharField(
        max_length=20,
        unique=True
    )
    barCode = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    lastPurchase = models.DateField(null=True, blank=True)
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    measurementUnits = models.ForeignKey(MeasurementUnits, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.description)

    def save(self):
        self.description = self.description.upper()
        super(Product, self).save()

    class Meta: 
        verbose_name_plural = "Products"
        unique_together = ('code', 'barCode')

