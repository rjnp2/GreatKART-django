from django.db import models
from django.db.models import Avg, Count
from category.models import Category
from django.urls import reverse
from accounts.models import Account

# Create your models here.
class Product(models.Model):

    product_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    prod_images = models.ImageField(upload_to = 'pics/product')
    is_available = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    create_date =  models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        average = 0

        if reviews['average'] is not None:
            average = float(reviews['average'])

        return average

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0

        if reviews['count'] is not None:
            count = int(reviews['count'])

        return count


    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

class VariationManager(models.Manager):

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size',is_active=True)
        


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)
class Variation(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices= variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    create_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return str(self.variation_value)

class ReviewRating(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    review = models.TextField(max_length=255,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    prod_images = models.ImageField(upload_to = 'pics/store/product', max_length=255)

    class Meta:
        verbose_name = 'ProductGallery'
        verbose_name_plural = 'ProductGallery'

    def __str__(self):
        return self.product.product_name