from django.db import models

def category_pic_upload_path(instance, filename):
    return f"category_pics/category_{instance.id}/{filename}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True
    )
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    category_pic = models.ImageField(
        upload_to=category_pic_upload_path,
        default="category_pics/default_category.png",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        # Display like "Parent > Child"
        full_path = [self.name]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        return ' > '.join(full_path[::-1])

