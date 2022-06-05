from django.test import TestCase


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')        followers = profile.followers.all() for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False        number_of_followers = len(followers)        context = {
                    'user': user,
                    'profile': profile,
                    'posts': posts,
                    'is_following': is_following,
                    'number_of_followers': number_of_followers,
                }
        return render(request, 'social/profile.html', context)
