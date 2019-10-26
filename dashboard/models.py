from django.db import models
from account.models import Account
from django.db.models import Q

# Create your models here.

class Friend(models.Model):
	user_1 = models.ForeignKey(Account, related_name="user_1", null=True, on_delete=models.CASCADE)
	user_2 = models.ForeignKey(Account, related_name="user_2", null=True, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)
	date_requested = models.DateTimeField(verbose_name="date requested", auto_now_add=True)
	date_confirmed = models.DateTimeField(verbose_name="date confirmed", null=True)
	

	# @classmethod
	# def send_request(cls, user_1, user_2):

	# 	friend_request = cls.objects.create(
	# 		user_1 = user_1,
	# 		user_2 = user_2,
	# 		status = False
	# 	)
	# 	friend_request.save()
	# 	args = {
	# 		'status' : 200
	# 	}
	# 	return args


	# @classmethod
	# def accept_request(cls, current_user, other_user):
	# 	friend = cls.objects.get(Q(current_user=current_user) & Q(status = False))
	# 	friend.status = True
	# 	friend.save()


	# @classmethod
	# def remove_friend(cls, current_user, other_user):
	# 	friend = cls.objects.get(current_user=current_user)
	# 	friend.status = True
	# 	friend.save()

	# @classmethod
	# def get_friends(cls, current_user):
	# 	friends = cls.objects.get(Q(user_1 = current_user) & Q(status = True))
	# 	print("friends are ----------------------")
	# 	print(friends[0])
	# 	return friends

	# @classmethod
	# def get_friend_requests(cls, current_user):
	# 	friend_requests = cls.objects.get(Q(current_user = current_user) & Q(status = False))
	# 	return friend_requests