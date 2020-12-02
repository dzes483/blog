from django.forms import ModelForm
from blog.models import Article, Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body', 'email']

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image']
