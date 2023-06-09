from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Tags for the articles
TAGS = ((0, 'Real Time'), (1, 'Archive'))


class Article(models.Model):
    """
    Article model for press releases
    """
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                               related_name='press_releases')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite',
                                       default=None, blank=True)
    tags = models.IntegerField(choices=TAGS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    User comment model
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='comments')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                             related_name='commenter')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    subject = models.TextField()
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.subject


class Picture(models.Model):
    """
    Picture model for the gallery
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    alt = models.TextField(default='Release Eritrea gallery picture')
    image = CloudinaryField('image', default='temporary')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
