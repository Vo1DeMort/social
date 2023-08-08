from django.urls import path
from .import views

urlpatterns = [
    path('',views.home ,name='home'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),

    path('profile/',views.profile_page,name='profile'),
    path('post/',views.user_post,name='post'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),

]
