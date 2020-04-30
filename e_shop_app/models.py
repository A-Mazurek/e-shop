from django.db import models


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Promotion(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class ProductPromotion(models.Model):
    date = models.DateTimeField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    promotion_id = models.ForeignKey(Promotion, on_delete=models.CASCADE)


class Vendor(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=10, decimal_places=2)


class Commission(models.Model):
    date = models.DateTimeField()
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)


class OrderLine(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_description = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_vat_rate = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    full_price_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
