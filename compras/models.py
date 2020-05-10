from django.db import models
from bases.models import ModelClass
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from inventario.models import Product

class Supplier(ModelClass):
    description = models.CharField(
        max_length=100,
        unique=True
    )
    address = models.CharField(
        max_length=250,
        null=False, 
        blank=True
    )
    contact = models.CharField(
        max_length=100
    )
    phone = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    email = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    def __str__(self):
        return '{}'.format(self.description)

    def save(self):
        self.description = self.description.upper()
        super(Supplier, self).save()

    class Meta:
        verbose_name_plural = "Suppliers"

class AcquisitionHeader(ModelClass):
    acquisitionDate = models.DateField(null=True, blank= True)
    observation = models.TextField(blank=True, null=True)
    billNumber = models.CharField(max_length=100)
    billDate = models.DateField()
    subtotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    def __str__(self):
        return '{}'.format(self.observation)
    def save(self):
        self.observation = self.observation.upper()
        self.total = self.subtotal - self.discount
        super(AcquisitionHeader, self).save()
    class Meta:
        verbose_name_plural = "Acquisitions Header"
        verbose_name = "Acquisition Header"

class AcquisitionDetail(ModelClass):
    acquisition = models.ForeignKey(AcquisitionHeader, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)
    supplierPrice = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    def __str__(self):
        return '{}'.format(self.product)
    def save(self):
        self.subtotal = float(float(int(self.amount)) * float(self.supplierPrice))
        self.total = self.subtotal - float(self.discount)
        super(AcquisitionDetail, self).save()
    class Meta:
        verbose_name_plural = "Acquisitions Header"
        verbose_name = "Acquisition Header"

@receiver(post_delete, sender = AcquisitionDetail)
def acquisitionDetailDelete(sender, instance, **kwargs):
    id_product = instance.product.id
    id_acquisition = instance.acquisition.id 
    header = AcquisitionHeader.objects.filter(pk = id_acquisition).first()
    if header:
        subtotal = AcquisitionDetail.objects.filter(acquisition = id_acquisition).aggregate(Sum('subtotal'))
        discount = AcquisitionDetail.objects.filter(acquisition = id_acquisition).aggregate(Sum('discount'))
        header.subtotal = subtotal['subtotal__sum']
        header.discount = discount['discount__sum']
        header.save()
    product = Product.objects.filter(pk = id_product).first()
    if product:
        amount = int(product.stock) - int(instance.amount)
        product.stock = amount
        product.save()

@receiver(post_save, sender = AcquisitionDetail)
def acquisitionDetailSave(sender, instance, **kwargs):
    id_product = instance.product.id
    acquisitionDate = instance.acquisition.acquisitionDate
    product = Product.objects.filter(pk = id_product).first()
    if product:
        amount = int(product.stock) + int(instance.amount)
        product.stock = amount
        product.lastPurchase = acquisitionDate
        product.save()