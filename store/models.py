from django.db import models
from django.contrib.auth.models import User
from itertools import zip_longest
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
    singer_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.singer_name
'''Composer START'''
class Composer(models.Model):
    composer_name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.composer_name
class Conductor(models.Model):
    conductor_name = models.CharField(max_length=200, null=True, blank=True)
    orchestra_name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f'{self.conductor_name}, {self.orchestra_name}' if self.orchestra_name else self.conductor_name

'''Composer END'''


'''
Vynil Metadata START
'''

class RecordingCompany(models.Model):
    recording_company_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.recording_company_name

class VynilAudioType(models.Model): # stereo/mono
    audio_type_name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.audio_type_name

class Distributor(models.Model):
    distributor_name = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.distributor_name

'''
Vynil Metadata END
'''

class Label(models.Model):
    label_name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.label_name

class Factory(models.Model):
    factory_name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.factory_name

'''NEW START'''
class CountryOfProduction(models.Model):
    country_name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.country_name

class GenreOfRecording(models.Model):
    genre_name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.genre_name

class SizeName(models.Model):
    size_name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.size_name
class Size(models.Model):
    size = models.IntegerField(blank=True, null=True)
    size_name = models.OneToOneField(SizeName, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.size} мм ({self.size_name})'

class QualityLP(models.Model):
    quality_letter = models.CharField(max_length=200, null=True, blank=True)
    additional_info = models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
        return f'{self.quality_letter} ({self.additional_info})'

class QualityCover(models.Model):
    info = models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
        return self.info
'''NEW END'''


class Album(models.Model):
    album_name = models.CharField(max_length=200, null=True)
    singer = models.ForeignKey(Singer, on_delete=models.SET_NULL, blank=True, null=True)
    composer = models.ForeignKey(Composer, on_delete=models.SET_NULL, blank=True, null=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, blank=True, null=True)

    label = models.ForeignKey(Label, on_delete=models.SET_NULL, blank=True, null=True)
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, blank=True, null=True)


    '''NEW ALBUM METADATA START'''
    year_of_issue = models.IntegerField(null=True, blank=True)
    year_of_records_from = models.IntegerField(null=True, blank=True)
    year_of_records_to = models.IntegerField(null=True, blank=True)

    country_of_production = models.ForeignKey(CountryOfProduction, on_delete=models.SET_NULL, blank=True, null=True)
    recording_company = models.ForeignKey(RecordingCompany, on_delete=models.SET_NULL, blank=True, null=True)
    audio_type = models.ForeignKey(VynilAudioType, on_delete=models.SET_NULL, blank=True, null=True)
    distributor = models.ForeignKey(Distributor, on_delete=models.SET_NULL, blank=True, null=True)
    issue = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(GenreOfRecording, on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    quality_lp = models.ForeignKey(QualityLP, on_delete=models.SET_NULL, blank=True, null=True)
    quality_cover = models.ForeignKey(QualityCover, on_delete=models.SET_NULL, blank=True, null=True)


    '''NEW ALBUM METADATA END'''

    def __str__(self):
        return f'{self.singer}, {self.album_name}'

    @property
    def get_tracks(self):
        tracks = self.track_set.all()
        return tracks

    @property
    def get_tracks_sides(self):

        tracks = self.track_set.all()
        if len(tracks) == 0:
            return None
        track1 = tracks.filter(album_side__album_side_name=1)
        track2 = tracks.filter(album_side__album_side_name=2)
        if len(tracks) == len(track1) + len(track2):
            try:
                track_1_time = []
                track_2_time = []
                track_1_name = []
                track_2_name = []
                # track_1_no = []
                # track_2_no = []
                for track in track1:
                    track_1_name.append(track.track_name)
                    track_1_time.append(track.track_time)
                    # track_1_no.append(track.track_no)

                for track in track2:
                    track_2_name.append(track.track_name)
                    track_2_time.append(track.track_time)
                    # track_2_no.append(track.track_no)


                track_1_time_zipped = []
                for i in range(len(track_1_name)):
                    # track_no = track_1_no[i]
                    track = track_1_name[i]
                    time = track_1_time[i]
                    if time:
                        track_1_time_zipped.append(f'{track} - {time}')
                    else:
                        track_1_time_zipped.append(f'{track}')

                track_2_time_zipped = []
                for i in range(len(track_2_name)):
                    # track_no = track_2_no[i]
                    track = track_2_name[i]
                    time = track_2_time[i]
                    if time:
                        track_2_time_zipped.append(f'{track} - {time}')
                    else:
                        track_2_time_zipped.append(f'{track}')

                zipped_list = zip_longest(track_1_time_zipped,track_2_time_zipped, fillvalue='')
                return zipped_list
            except:
                return None
        return None


'''NEW START'''
class AlbumSide(models.Model):
    album_side_name = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f'{self.album_side_name}'

'''NEW END'''


class Track(models.Model):
    track_no = models.IntegerField(null=True, blank=True)
    track_name = models.CharField(max_length=200, null=True)
    track_time = models.FloatField(null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    '''New'''
    album_side = models.ForeignKey(AlbumSide, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['id']


    def __str__(self):
        return f'{self.track_name} - {self.track_time}' if self.track_time else self.track_name


class ProductDescription(models.Model):
    singer = models.ForeignKey(Singer, on_delete=models.SET_NULL, blank=True, null=True)
    composer = models.ForeignKey(Composer, on_delete=models.SET_NULL, blank=True, null=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.singer:
            return f'{self.singer} - {self.album}'
        else:
            return f'{self.composer} - {self.conductor} -  {self.album}'
'''
Product Description END
'''

class Product(IsActiveMixin, models.Model):
    custom_id = models.IntegerField(default=100, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    description = models.ForeignKey(ProductDescription, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image1 = models.ImageField(upload_to='store',null=True, blank=True)
    image2 = models.ImageField(upload_to='store',null=True, blank=True)

    quantity = models.IntegerField(default=1, blank=True, null=True)

    custom_info = models.TextField(blank=True, null=True)


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






