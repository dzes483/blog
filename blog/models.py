from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False,
                            null=False, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name = 'articles')
    date_posted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    body = models.TextField()
    image = models.ImageField(blank=True)

    class Meta:
        ordering = ['-date_posted']

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug,
        }
        return reverse('article_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='comments')
    name = models.CharField(max_length=50, blank=False)
    body = models.TextField(max_length=1000)
    email = models.EmailField(max_length=254, blank=False)
    date_posted = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 's'
        ordering = ['date_posted']

    def __str__(self):
        return self.Comment

    def get_absolute_url(self):
        """Returns the url to access a detail record for the post"""
        return reverse('forum:post_detail', args=[str(self.id)])

    def __unicode__(self):
        return self.Comment
