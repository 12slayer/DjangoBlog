from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect

# Create your views here.

from .models import BlogPost,Comment
from django.shortcuts import Http404

from .form import ContactForm,CommentForm
from .blogform import BlogPostModelForm , AppUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from .registerform import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from .models import AppUser,Like

def test(request):
    return render(request, "n.html", {})


@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='appuser')
            user.groups.add(group)
            AppUser.objects.create(
                user=user,
            )
            messages.success(request, "account was created " +username)
            return redirect('login')



    context = {'form': form}
    return render(request, "account/register.html", context)

@unauthenticated_user
def loginpage(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, "user name or password is incorrect")





    return render(request, "account/login.html", {})


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['appuser'])
def userProfile(request):
    appuser = request.user.appuser
    form = AppUserForm(instance=appuser)
    profile=AppUser.objects.all().count()
    if request.method == 'POST':
        form = AppUserForm(request.POST, request.FILES, instance=appuser)
        if form.is_valid():
            form.save()
    context = {'form': form, "profile": profile}
    return render(request, 'account/userProfile.html', context)







def contact_page(request):
    print(request.POST)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()


    context = {
        "title": "contact us", "form": form
    }

    return render(request, "contact.html", context)


def blog_post_list_view(request):
    #listview can list out object

    qs = BlogPost.objects.all().published()  #filter(title__icontains='welcome')
    #qs = BlogPost.objects.filter(publish_date__lte=now)
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user.appuser)
        qs = (qs | my_qs).distinct()

    template_name = "blog_post_list.html"
    context = {"object_list": qs}
    return render(request, template_name, context)


def userPost(request):
    user_posts = BlogPost.objects.filter(user=request.user.appuser)
    context = {"userblog": user_posts}
    return render(request, "userPost.html", context)


def blog_post_details_view(request,id):
    obj = BlogPost.objects.get(id=id)




    user = request.user
    appUser = AppUser.objects.get(user=user)
    comments = Comment.objects.filter(post_id=obj)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)

            new_comment.post_id = obj
            new_comment.user_id = appUser

            new_comment.save()


    else:
        comment_form = CommentForm()
    template_name = "blog_post_details_page.html"
    context = {"object": obj,'comments': comments,'new_comment': new_comment,'comment_form': comment_form,'user':appUser}
    return render(request, template_name, context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['appuser'])
def blog_post_update_view(request, id):
    obj = get_object_or_404(BlogPost, id=id)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
      form.save()

        
    template_name = "create.html"
    context = {'form': form, "title": f"Update {obj.title}"}
    return render(request, template_name, context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['appuser'])
def blog_post_create_view(request):

    #if not request.user.is_authenticated:
        #return render(request, 'not-a-user.html', {})

    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user.appuser
        obj.save()


        context = {'form': form}
    return render(request, "create.html", {'form': form})




@login_required(login_url='login')
@allowed_users(allowed_roles=['appuser'])
def blog_post_delete_view(request, id):
    obj = get_object_or_404(BlogPost,id=id)
    template_name = "delete.html"
    if request.method =='POST':
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)


def home_page(request):
    my_title = "hello there"
    qs = BlogPost.objects.all()[:5]
    context = {"title": my_title, 'blog_list': qs}

    return render(request, "home.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admin_page(request):
    appuser = AppUser.objects.all()
    template = "account/admin.html"
    context = {"appuser": appuser}
    return render(request, template, context)


def deleteUser(request, pk):
    appuser = AppUser.objects.get(id=pk)
    if request.method == "POST":
        appuser.delete()
        return redirect('/admintem')
    context = {'appuser': appuser}
    return render(request, 'account/delete.html', context)



def like_post(request):
    user = request.user

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = BlogPost.objects.get(id=post_id)
        appUser = AppUser.objects.get(user=user)
    if appUser in post_obj.liked.all():
        post_obj.liked.remove(appUser)
    else:
        post_obj.liked.add(appUser)


    like, created = Like.objects.get_or_create(user=appUser, post_id=post_id)

    if not created:
        if like.value == "Unlike":
            like.value == "Like"
        else:
            like.value = "Like"


    else:
        like.value = 'Like'

    post_obj.save()
    like.save()

    return redirect("details", id=post_id)



