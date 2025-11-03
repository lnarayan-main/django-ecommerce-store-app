from django.db import models
from django.utils.text import slugify
from account.models import User 

from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy

from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('core.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)

    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=False, related_name='products')

    available_sizes = models.ManyToManyField(
        'Size', 
        related_name='products',
        help_text="Select all sizes this product is sold in."
    ) 
    available_colors = models.ManyToManyField(
        'Color', 
        related_name='products',
        help_text="Select all colors this product is sold in."
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = f"SKU-{self.pk or ''}-{slugify(self.name)[:20]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Brand(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True, 
        help_text="The official name of the product brand."
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True, 
        blank=True, 
        editable=False, 
        help_text="URL-friendly name for SEO."
    )

    logo = CloudinaryField('image', blank=True, null=True)

    is_active = models.BooleanField(
        default=True, 
        help_text="Designates whether this brand is currently active."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Auto-generate or update slug
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)

        # Delete old logo from Cloudinary if replaced
        try:
            old = Brand.objects.get(pk=self.pk)
            if old.logo and old.logo != self.logo:
                destroy(old.logo.public_id)
        except Brand.DoesNotExist:
            pass  # First save, no old logo

        super().save(*args, **kwargs)


# --- 2. Size Model ---
class Size(models.Model):
    name = models.CharField(
        max_length=15, 
        unique=True,
        help_text="The size label (e.g., S, M, L, 10, 32x30)."
    )
    display_order = models.IntegerField(
        default=0,
        help_text="The numerical order for sorting (e.g., S=1, M=2, L=3)."
    )

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        ordering = ('display_order', 'name')

    def __str__(self):
        return self.name


# --- 3. Color Model ---
class Color(models.Model):
    name = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="The common name of the color (e.g., Red, Navy, Olive)."
    )
    hex_code = models.CharField(
        max_length=7, 
        unique=True, 
        null=True, 
        blank=True,
        help_text="HTML Hex code for display (e.g., #FF0000 for Red)."
    )

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # image = models.ImageField(upload_to='products/%Y/%m/%d/')
    image = CloudinaryField('image')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    
    def save(self, *args, **kwargs):
        try:
            old = ProductImage.objects.get(pk=self.pk)
            if old.image and old.image != self.image:
                destroy(self._get_public_id(old.image.url))
        except ProductImage.DoesNotExist:
            pass  # New image, nothing to delete
        super().save(*args, **kwargs)

    def _get_public_id(self, url):
        """
        Extract Cloudinary public_id from the image URL.
        Assumes default Cloudinary URL format.
        """
        from urllib.parse import urlparse
        import os

        path = urlparse(url).path  # /your_cloud_name/image/upload/v1234567890/folder/image.jpg
        public_id = os.path.splitext(path.split('/upload/')[-1])[0]  # remove extension
        return public_id
    


@receiver(pre_delete, sender=ProductImage)
def delete_image_from_cloudinary(sender, instance, **kwargs):
    if instance.image:
        destroy(instance._get_public_id(instance.image.url))



