from django.db import models
from category.models import Category
from django.urls import reverse

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
    
    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
