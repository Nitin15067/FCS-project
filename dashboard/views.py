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


def wallet_view(request):

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


def friends_view(request):
	user_1 = request.user
	friends = (Friend.objects.filter(user_1 = user_1) | Friend.objects.filter(user_2 = user_1) ) & Friend.objects.filter(status = True)

	args = {
		'friends' : friends,
		'status' : 200,
		'errors' : ''
	}

	return render(request, 'friends.html', args)

def friend_requests_view(request):

	user_1 = request.user
	friend_requests = Friend.objects.filter(user_2 = user_1) & Friend.objects.filter(status = False)

	args = {

		'friend_requests' : friend_requests,
		'status' : 200,
		'errors' : ''
	}

	return render(request, 'friend_request.html', args)

def send_request_view(request, u_id):
	args = {

	}
	user_1 = request.user
	user_2 = Account.objects.filter(id=u_id)[0]

	if Friend.objects.filter(user_1 = user_1, user_2 = user_2).exists() | Friend.objects.filter(user_1 = user_2, user_2 = user_1).exists():
		return redirect('friends')
	else : 
		friend_request = Friend(user_1 = user_1, user_2 = user_2, status = False)
		friend_request.save()

	return redirect('friends')
	
def accept_request_view(request, u_id):

	user_2 = request.user
	user_1 = Account.objects.filter(id=u_id)[0]

	accept_request = Friend.objects.get(user_1 = user_1, user_2 = user_2, status = False)
	accept_request.status = True
	accept_request.save()	
	return redirect('friends')

def delete_request_view(request, u_id):

	user_2 = request.user
	user_1 = Account.objects.filter(id=u_id)[0]

	delete_request = Friend.objects.get(user_1 = user_1, user_2 = user_2)
	delete_request.delete()
	delete_request.save()

	return redirect('friend_requests')

def unfriend_view(request, u_id):

	user_1 = request.user
	user_2 = Account.objects.filter(id=u_id)[0]

	remove_friend = Friend.objects.get(user_1 = user_1, user_2 = user_2)
	remove_friend.delete()
	remove_friend.save()

	return redirect('friends')


	
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
