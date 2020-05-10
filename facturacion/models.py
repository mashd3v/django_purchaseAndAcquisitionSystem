from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from bases.models import ModelClass, ModelClass2
from inventario.models import Product

class Customer(ModelClass):
    NAT = 'Natural'
    JUR = 'Juristic'
    CUSTOMER_TYPE = [
        (NAT, 'Natural'),
        (JUR, 'Juristic')
    ]
    names = models.CharField(max_length=100) 
    lastNames = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20, 
        null=True, 
        blank=True)
    customerType = models.CharField(
        max_length=10,
        choices=CUSTOMER_TYPE,
        default=NAT
    )
    def __str__(self):
        return '{} {}'.format(self.lastNames, self.names)
    def save(self):
        self.names = self.names.upper()
        self.lastNames = self.lastNames.upper()
        super(Customer, self).save()
    class Meta:
        verbose_name_plural = "Customers"

class BillingHeader(ModelClass2):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    subtotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    def __str__(self):
        return '{}'.format(self.id)
    def save(self):
        self.total = self.subtotal - self.discount
        super(BillingHeader, self).save()
    class Meta:
        verbose_name_plural = "Billings Header"
        verbose_name = "Billing Header"
        permissions = [
            ('cashier_supervisor_billingheader', 'Cashier Supervisor Permissions')
        ]

class BillingDetail(ModelClass2):
    billing = models.ForeignKey(BillingHeader, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)
    price = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    def __str__(self):
        return '{}'.format(self.product)
    def save(self):
        self.subtotal = float(float(int(self.amount)) * float(self.price))
        self.total = self.subtotal - float(self.discount)
        super(BillingDetail, self).save()
    class Meta:
        verbose_name_plural = "Billings Details"
        verbose_name = "Billing Detail"
        permissions = [
            ('cashier_supervisor_billingdetail', 'Cashier Supervisor Permissions')
        ]

@receiver(post_save, sender = BillingDetail)
def billingDetailSave(sender, instance, **kwargs):
    billingId = instance.billing.id
    productId = instance.product.id
    head = BillingHeader.objects.get(pk=billingId)
    if head:
        subtotal = BillingDetail.objects\
            .filter(billing=billingId)\
            .aggregate(subtotal=Sum('subtotal'))\
            .get('subtotal', 0.00)
        discount = BillingDetail.objects\
            .filter(billing=billingId)\
            .aggregate(discount=Sum('discount'))\
            .get('discount', 0.00)
        head.subtotal = subtotal
        head.discount = discount
        head.save()
    product = Product.objects.filter(pk=productId).first()
    if product:
        amount = int(product.stock) - int(instance.amount)
        product.stock = amount
        product.save()
