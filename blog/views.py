from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from blog.forms import CommentForm, ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

class ArticleList(ListView):
    queryset = Article.objects.order_by('-date_posted')
    template_name = 'blog/index.html'

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title','body', 'image']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

def article_detail(request, pk, slug):
    template_name = 'blog/article_detail.html'
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.filter(active=True)
    request.session['num_comments'] = article.comments.all().count()
    num_comments = request.session['num_comments']
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.article = article
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'article': article,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'num_comments': num_comments,})

@login_required
def update_article(request, pk, slug):
    obj = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, request.FILES or None,
                       instance=obj)
    if request.method == 'POST':
        if form.is_valid():
           form.save()
           return redirect('article_detail', pk=pk, slug=slug)
    return render(request, 'blog/article_update.html', {'form': form})

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'blog/article_update.html'
    form_class = ArticleForm
    success_url = 'article_detail'

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:home')


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('blog:article_detail')
