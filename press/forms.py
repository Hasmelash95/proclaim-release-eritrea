from .models import Comment, Article
from django import forms
from django_summernote.fields import SummernoteWidget, SummernoteTextField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class ArticleForm(forms.ModelForm):
    """
    Creates a form the staff can fill out on the site to
    post articles.
    """
    title = forms.CharField(label='Title:', required=True,
                            widget=forms.Textarea(attrs={'rows': 1,
                                                  'cols': 80}))
    content = SummernoteTextField()
    excerpt = forms.CharField(label='Excerpt:', required=False,
                              widget=forms.Textarea(attrs={
                                                    'rows': 4,
                                                    'cols': 80
                                                    }))
    published_on = forms.DateField(
        label='Published on:', required=False,
        help_text='Leave blank to use today. Use the original date for '
                  'older releases.',
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    slug = forms.TextInput()

    class Meta:
        model = Article
        widgets = {
            'content': SummernoteWidget(),
        }
        labels = {
            'content': 'Content:',
            'tags': 'Tags:'
        }
        fields = ['title', 'published_on', 'content', 'excerpt', 'tags']

    def clean_published_on(self):
        # A blank date keeps the article's current date, or today for
        # a new article
        published_on = self.cleaned_data.get('published_on')
        if published_on:
            return published_on
        if self.instance.pk:
            return self.instance.published_on
        return timezone.localdate()


class CommentForm(forms.ModelForm):
    """
    Creates a form logged in users can fill out underneath
    articles that will be sent to the database to be approved.
    """
    subject = forms.CharField(widget=forms.Textarea(attrs={'rows': 1,
                              'cols': 80}))

    class Meta:
        model = Comment
        fields = ['subject', 'content']
