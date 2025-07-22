from django.db import models

# Create your models here.
# title , category , ad , suscribe , most popularr


# Post :  title , content , feature_image , author , views_count , category ,

# tags : many to many 

# comments : many to one 

# categoy : one to many FOreignKey



class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True # Don't create table in DB
        
class Category(TimeStampModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null = True , blank = True)
    description = models.TextField(null = True , blank = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"] # Category.objects.all() => name wise ordering 
        verbose_name = "category"
        verbose_name_plural = "Categories" # Add this line 
        
class Tag(TimeStampModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        '''
        Return a string representation of the Tag , which is its name
        '''
        return self.name
    
class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("activate","Active"),
        ("in_activate","Inactive"),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d",blank=False) # blank = false rakhnai parne 
    author = models.ForeignKey("auth.User",on_delete= models.CASCADE) # on_delete , author delete bhayo bhane sab kura dlete hunxa 
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    is_breaking_news = models.BooleanField(default=False)
    published_at = models.DateTimeField(null = True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # category delete bhayo bhane sab delete hunxa 
    tag = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.title
    
    
# tag - post 
# 1 post can have M tags => M
# 1 tag can be associated with M post => M
# M TO M => ManyToManyField , post 