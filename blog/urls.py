"""ok URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from searches.views import search_view
from django.contrib.auth import views as auth_views


from .views import (
    contact_page,
    home_page,
    blog_post_list_view,
    blog_post_details_view,
    blog_post_update_view,
    blog_post_create_view,
    blog_post_delete_view,
    register,
    loginpage,
    logoutUser,
    userProfile,
    admin_page,
    deleteUser,
    test,
    userPost,
    like_post
)

urlpatterns = [
    path('blog/<str:id>/', blog_post_details_view ,name="details"),
    path('blog/<str:id>/edit/', blog_post_update_view),
    path('blog/<str:id>/delete/', blog_post_delete_view),
    path('blog-new/', blog_post_create_view),#,include('blog.urls'))
    path('blog', blog_post_list_view),
    path('admin/', admin.site.urls),
    path('contact', contact_page),
    path('', home_page, name="home"),
    path('search/', search_view),
    path('register', register, name="register"),
    path('login', loginpage, name="login"),
    path('logout', logoutUser, name="logout"),
    path('account', userProfile, name="account"),
    path('admintem', admin_page, name="admin"),
    path('delete/<str:pk>', deleteUser, name="delete_appuser"),
    path('userpost', userPost),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="account/password_resent_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_success_complete', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"),
         name="password_reset_complete"),

    path('like', like_post, name="like-post-view")


]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
