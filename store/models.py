from django.db import models
from django.utils import timezone
from utilities.constants import BUSINESS_TYPE_CHOICES, STATE_CHOICES
from owner.models import BusinessOwner


class Store(models.Model):
    title = models.CharField(max_length=32)
    logo = models.ImageField(upload_to='logo_images/', null=True)
    business_type = models.IntegerField(choices=BUSINESS_TYPE_CHOICES)
    business_owner = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE, related_name='stores')
    owner_phone_number = models.CharField(blank=True,max_length=20)

    address = models.TextField(null=True,blank=True)
    state = models.IntegerField(choices=STATE_CHOICES)
    city = models.CharField(max_length=32, null=True)
    telephone_number = models.CharField(max_length=20)

    tables_count = models.PositiveSmallIntegerField()
    subscription_factor = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    instagram_page_link = models.CharField(max_length=32, null=True,blank=True)
    telegram_channel_link = models.CharField(max_length=32, null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            self.owner_phone_number = self.business_owner.phone_number
            return super().save(*args, **kwargs)
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Collection(models.Model):
    title = models.CharField(max_length=32)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='collections')
    is_featured = models.BooleanField(default=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            return super().save(*args, **kwargs)
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.store}.{self.title}"


class Product(models.Model):
    title = models.CharField(max_length=32)
    image = models.ImageField(upload_to='products_images/', null=True)
    description = models.TextField(null=True)
    unit_price = models.DecimalField(max_digits=15, decimal_places=3)

    inventory = models.PositiveSmallIntegerField(null=True)
    is_available = models.BooleanField(default=False, null=False, blank=False)
    is_featured = models.BooleanField(default=False, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            self.store = self.collection.store
            return super().save(*args, **kwargs)
        else:
            self.updated_at = timezone.now()
            return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.store}.{self.title}"


class Comment(models.Model):
    name = models.CharField(max_length=32, default='ناشناس')
    content = models.TextField()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            return super().save(*args, **kwargs)
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} from {self.name} : {self.amount}"


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
