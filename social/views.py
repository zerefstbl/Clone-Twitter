from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.contrib.auth.models import User


from .forms import PostForm, CommentForm
from .models import Post, Comment, Profile

from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from django.views.generic.edit import UpdateView, DeleteView


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-create_on')
        form = PostForm()

        user = self.request.user

        profile = Profile.objects.get(pk=user.pk)

        usuarios = User.objects.all().order_by('-pk')

        followers = profile.followers.all()

        number_of_followers = len(followers)

        context = {'post_list': posts, 'form': form,
                   'profile': profile, 'user': user, 'usuarios': usuarios, 'followers': number_of_followers}

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-create_on')
        form = PostForm(request.POST)

        user = self.request.user

        profile = Profile.objects.get(pk=user.pk)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        usuarios = User.objects.all().order_by('-pk')

        context = {'post_list': posts, 'form': form,
                   'profile': profile, 'user': user, 'usuarios': usuarios}

        return render(request, 'social/post_list.html', context)


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {'post': post, 'form': form, 'comments': comments}

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        print(form)

        context = {'post': post, 'form': form, 'comments': comments}

        return render(request, 'social/post_detail.html', context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'social/post_delete.html'
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'social/post_edit.html'
    model = Post
    fields = ['body']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-create_on')

        followers = profile.followers.all()

        is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            elif follower != request.user:
                is_following = False

        number_of_followers = len(followers)

        context = {'user': user, 'posts': posts, 'profile': profile,
                   'is_following': is_following, 'number_of_followers': number_of_followers}

        return render(request, 'social/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)

        profile.followers.add(request.user)

        return redirect('profile', pk=profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        profile = Profile.objects.get(pk=pk)

        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)
