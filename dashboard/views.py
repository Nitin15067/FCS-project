from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from dashboard.forms import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from account.models import Account
from dashboard.models import Friend

# from dashboard.models import Friends

def dashboard_view(request):
	args = {
		"text" : "This is the dashboard"
	}

	accounts = Account.objects.all()
	args['accounts'] = accounts 

	if request.user.is_authenticated:
		return render(request, 'dashboard.html', args)
	else : return redirect('login')

def profile_view(request, u_id=None):

	if u_id:
		user_data = Account.objects.filter(id=u_id)[0]

	print(user_data)

	args = {
		'user': user_data
	}
	return render(request, 'profile.html', args)

def edit_profile_info_view(request):
	args = {}

	if request.method == "POST":
		form = EditProfileForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			return redirect('profile')
	
	else:
		form = EditProfileForm(instance=request.user)
		args = {'edit_profile_info_form': form}
		return render(request, 'edit_profile_info.html', args)

def change_password_view(request):
	args = {}

	if request.method == "POST":
		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('profile') 
		else: return redirect('change_password')
	else: 
		form = PasswordChangeForm(user=request.user)
		args = {'change_password_form': form}
		return render(request, 'change_password.html', args)


def friends_view(request):
	current_user = request.user
	friends = Friend.get_friends(current_user)
	for friend in friends.users.all():
		print (friend)
		
	args = {
		'friends' : friends,
		'status' : 200,
		'errors' : ''
	}
	print(args['friends'])

	return render(request, 'friends.html', args)

def wallet_view(request):

	# balance = 500
	# send = 1
	# receive = 0
	# send_to = 'Rakesh'
	# receive_from = ''
	# time = 'fsd'
	# date = 'sdf',
	# payment_id = 'sfd'
	# payment_method = 'sdg'
	# status = 0


	# transactions = {
	# 	't_id' : t_id
	# 	'send' : send,
	# 	'receive' : receive,
	# 	'send_to' : send_to,
	# 	'receive_from' : receive_from
	# 	'time' : time,
	# 	'date' : date,
	# 	'payment_id' : payment_id,
	# 	'payment_method' : payment_method,
	# 	'status' : status,
	# }

	balance = 556
	transactions = 'ergsdg'

	args = {
		'balance' : balance,
		'transactions' : transactions

	}
	return render(request, 'wallet.html', args)

def search_view(request):

	
	search_content = request.GET.get('q')
	# print(request.user.id)


	if search_content:
		results = Account.objects.filter(
			Q(username__icontains=search_content)
			| Q (email__icontains=search_content)
			| Q (first_name=search_content)
			)
		results = results.exclude(id=request.user.id)


		if results:
			args = {
				'result' : results,
				'status' : 200,
				'error' : '' 
			}
			return render(request, 'search.html', args)
		else:
			args = {
				'result' : '',
				'status' : 0,
				'error' : {
					1 : 'No results found'
				}

			}
			return render(request, 'search.html', args)
	return render(request, 'search.html')


def add_friend_view(request, u_id):
	args = {
	
	}

	current_user = request.user
	other_user = Account.objects.filter(id=u_id)[0]


	friend_request = Friend.send_request(current_user, other_user)


	print("friend request send")
	# request_username = request.GET.get('')
	return render(request, 'add_friend.html', args)


def transfer_money_view(request):
	args = {
	
	}
	return render(request, 'transfer_money.html', args)

def transactions_view(request):
	args = {
	
	}	
	return render(request, 'transactions.html', args)

def add_money_view(request):
	args = {
	
	}	
	return render(request, 'add_money.html', args)

def messenger_view(request):
	args = {
	
	}	
	return render(request, 'add_money.html', args)

def create_group_view(request):
	args = {
	
	}	
	return render(request, 'add_money.html', args)
