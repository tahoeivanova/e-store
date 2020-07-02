from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class ProductManager(models.Manager):
    def get_queryset(self):
        all_objects = super().get_queryset()
        return all_objects.filter(is_active=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
'''
Product Description START
'''
class Singer(models.Model):
    singer_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.singer_name

class Label(models.Model):
    label_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.label_name

class Factory(models.Model):
    factory_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.factory_name

class Album(models.Model):
    album_name = models.CharField(max_length=200, null=True)
    singer = models.ForeignKey(Singer, on_delete=models.SET_NULL, blank=True, null=True)
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, blank=True, null=True)
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, blank=True, null=True)
    year_of_records = models.CharField(max_length=20, null=True, blank=True)
    year_of_release = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.album_name

    @property
    def get_tracks(self):
        tracks = self.track_set.all()
        return tracks


class Track(models.Model):
    track_no = models.IntegerField(null=True, blank=True)
    track_name = models.CharField(max_length=200, null=True)
    track_time = models.FloatField(null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.track_name


class ProductDescription(models.Model):
    singer = models.ForeignKey(Singer, on_delete=models.SET_NULL, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.singer} - {self.album}'
'''
Product Description END
'''

class Product(IsActiveMixin, models.Model):
    custom_id = models.IntegerField(default=100, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    description = models.ForeignKey(ProductDescription, on_delete=models.CASCADE, blank=True, null=True)
    quality = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image1 = models.ImageField(upload_to='store',null=True, blank=True)
    image2 = models.ImageField(upload_to='store',null=True, blank=True)

    '''NEW'''
    quantity = models.IntegerField(default=1, blank=True, null=True)
    '''NEW'''

    objects = models.Manager()
    product_active = ProductManager()
    class Meta:
        ordering = ['custom_id']

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url

    @property
    def imageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address






