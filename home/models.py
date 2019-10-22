from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from account.models import Account
# from django.urls import reverse

# Create your models here.
class feed(models.Model):
    # u_id = models.IntegerField()
    # title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    post_to = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True,related_name="other_users")

    def __str__(self):
        return self.author.first_name

