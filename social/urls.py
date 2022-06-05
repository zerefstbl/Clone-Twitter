from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/edit/<int:pk>', views.PostEditView.as_view(), name='post_edit'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>',
         views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/followers/add',
         views.AddFollower.as_view(), name='add_follower'),
    path('profile/<int:pk>/follower/remove',
         views.RemoveFollower.as_view(), name='remove_follower'),
    path('post/<int:pk>/like', views.AddLike.as_view(), name='like'),
    path('post/<int:pk>/deslikes', views.AddDeslike.as_view(), name='deslike'),
    path('search/', views.ProfileSearch.as_view(), name='search_profile'),
]
