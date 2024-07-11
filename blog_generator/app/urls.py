from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.homepage, name='home'),
    path('signup', view=views.user_signup, name='signup_'),
    path('login', view=views.user_login, name='login_'),
    path('generate', view=views.generate_blog, name='blog_gen_'),
    path('all-blogs', view=views.all_blogs, name='all_blogs_'),
    path('blog-details/<int:pk>', view=views.blog_details, name='blog_details_'),
    path('logout', view=views.user_logout, name='logout_'),
]