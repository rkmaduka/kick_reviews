import os
import uuid
def upload_to_location(instance,filename):
    blocks = filename.split('.')
    ext = blocks[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    instance.title = blocks[0]
    return os.path.join('uploads/', filename)
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse 
VISIBILITY_CHOICES = (
(0, 'Public'),
(1, 'Anonymous'),
)
RATING_CHOICES = (
(0, 'None'),
(1, '*'),
(2, '**'),
(3, '***'),
(4, '****'),
(5, '*****'),
)
# Create your models here.
class Review(models.Model):
    sneaker = models.CharField(max_length=300)
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    image_file = models.ImageField(upload_to=upload_to_location, null=True, blank=True)
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default=0)
    
    def __unicode__(self):
     return self.sneaker

    def get_absolute_url(self):
     return reverse( "review_detail", args=[self.id])
    
    

class Comments(models.Model):
    review = models.ForeignKey(Review) 
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default=0)
    
    def _unicode_(self):
        return self.text  
    
    
  
class Vote(models.Model):
    user = models.ForeignKey(User)
    review = models.ForeignKey(Review, blank=True, null=True)
    comments = models.ForeignKey(Comments, blank=True, null=True)
    
    def _unicode_(self):
        return "%s upvoted" % (self.user.username)
        
        