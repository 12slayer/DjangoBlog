from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User











class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(content__icontains=query)

        )

        return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)
    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


# Create your models here.
class AppUser(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='image/', default='image/s.jpg', blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def getnumberofpost(self):
        return self.posts.all().count()

    def getUsersPost(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked = total_liked+1
        return total_liked

    def get_likes_recived_no(self):
        posts = self.posts.all()
        for item in posts:
            total_liked = item.liked.all().count()
            return total_liked


class BlogPost(models.Model):
    user = models.ForeignKey(AppUser, null=True,on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField(max_length=120)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    liked = models.ManyToManyField(AppUser, default=None, blank=True, related_name="likes")
    objects = BlogPostManager()

    class Meta:
        ordering = ['-publish_date', '-updated', '-timestamp']



    def getname(self):
        return self.user.name
    def get_absolute_url(self):
        return f"/blog/{self.id}"

    def get_edit_url(self):
        return f"/blog/{self.id}/edit"

    def get_delete_url(self):
        return f"/blog/{self.id}/delete"

    def countcomment(self):
        return self.comment_set.all().count()

    @property
    def num_likes(self):
        return self.liked.all().count()






class Comment(models.Model):
    post_id = models.ForeignKey(BlogPost, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(AppUser, null=True,on_delete=models.CASCADE,related_name="comment")

    class Meta:
        ordering = ['date_comment']

    def getnameing(self):
        return self.user_id.name

    def getImage(self):
        return self.user_id.profile_pic




Like_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)

class Like(models.Model):
    user = models.ForeignKey(AppUser, null=True,on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, null=True, on_delete=models.CASCADE)
    value = models.CharField(choices=Like_CHOICES, default='Like', max_length=10)


    def __str__(self):
        return f"{self.user}--{self.post}--{self.value}"
