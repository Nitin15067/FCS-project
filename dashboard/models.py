from django.db import models
from account.models import Account
from django.db.models import Q

# Create your models here.

class Friend(models.Model):
	current_user = models.ForeignKey(Account, related_name="owner", null=True, on_delete=models.CASCADE)
	users = models.ManyToManyField(Account, related_name="friend_list")
	status = models.BooleanField(default=False)
	date_requested = models.DateTimeField(verbose_name="date requested", auto_now_add=True)
	date_confirmed = models.DateTimeField(verbose_name="date confirmed", null=True)

	@classmethod
	def send_request(cls, current_user, other_user):
		friend, created = cls.objects.get_or_create(
			current_user = current_user
		)
		friend.users.add(other_user)
		friend.status = False
		friend.save()


	@classmethod
	def accept_request(cls, current_user, other_user):
		friend = cls.objects.get(current_user=current_user)
		friend.status = True
		friend.save()

	@classmethod
	def remove_friend(cls, current_user, other_user):
		friend = cls.objects.get(current_user=current_user)
		friend.status = True
		friend.save()

	@classmethod
	def get_friends(cls, current_user):

		friends = cls.objects.filter(Q(current_user = current_user) & Q(status = False))[0]
		return friends

	@classmethod
	def get_friend_requests(cls, current_user):
		friends = cls.objects.filter(Q(current_user = current_user) & Q(status = False))
		return friend_requests