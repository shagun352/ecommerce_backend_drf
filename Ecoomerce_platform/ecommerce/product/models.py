from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    c_name = models.CharField(max_length = 250)
    slug = models.SlugField(max_length=40)

    def __str__(self) -> str:
        return self.c_name


    # def save(self, **kwargs):
    #     self.slug = slugify(self.c_name)
    #     super(Category, self).save(**kwargs)



class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
