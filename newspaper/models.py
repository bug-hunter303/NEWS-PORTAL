from django.db import models

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # Don't care table in DB

class Category(TimeStampModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100 , null=True , blank=True)
    description = models.TextField(null=True , blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"] # category.objects.null => ordering by name in ascending 
        verbose_name = "category" # singular text ko lagi admin site ma 
        verbose_name_plural = "Categories" # add this line 

class Tag(TimeStampModel):
    name = models.CharField(max_length= 100)

    def __str__(self):
        '''
        Return a string representation of the tag , which is its name 
        '''
        return self.name
    
class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("active","Active"),
        ("in_active", "Inactive"),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False) # post image bhanne folder baanxa aani yyyy/mm/dd bhaera basxa 
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    is_breaking_news = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Category mathi ko cat sanga associate gareko 
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    

