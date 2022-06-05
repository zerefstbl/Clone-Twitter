from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': '3', 'placeholder': 'Diga o que esta pensando...'}))

    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['body', 'image']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': '2', 'placeholder': 'Deixe seu recado...', }))

    class Meta:
        model = Comment
        fields = ['comment']
