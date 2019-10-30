from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from dashboard.forms import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from account.models import Account
from dashboard.models import Friend, Wallet, Transaction, feed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

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

	user_data = Account.objects.filter(id=u_id)[0]

	posts = feed.objects.filter(post_to = user_data).order_by('-date_posted')

	is_friend = False

	if int(u_id) == int(request.user.id):
		is_friend = True

	if Friend.objects.filter(user_1 = user_data, user_2 = request.user).exists() | Friend.objects.filter(user_2 = user_data, user_1 = request.user).exists():
		is_friend = True
	print(is_friend)

	args = {
		'user': user_data,
		'u_id' : int(u_id),
		'posts' : posts,
		'is_friend' : is_friend
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

	user_1 = Account.objects.filter(id=u_id)[0]
	user_2 = request.user

	if Friend.objects.filter(user_1 = user_1, user_2 = user_2).exists():
		Friend.objects.filter(user_1 = user_1, user_2 = user_2).delete()

	if Friend.objects.filter(user_1 = user_2, user_2 = user_1).exists():
		Friend.objects.filter(user_1 = user_2, user_2 = user_1).delete()
	# delete_request.save()

	return redirect('friend_requests')

def unfriend_view(request, u_id):

	user_1 = request.user
	user_2 = Account.objects.filter(id=u_id)[0]
	print(user_1)
	print(user_2)
	print("inside here ----------")
	# remove_friend_2 = Friend.objects.filter(user_1 = user_2, user_2 = user_1)[0] |  Friend.objects.filter(user_1 = user_1, user_2 = user_2)[0] 

	if Friend.objects.filter(user_1 = user_2, user_2 = user_1).exists():
		Friend.objects.filter(user_1 = user_2, user_2 = user_1)[0].delete()
	

	if Friend.objects.filter(user_1 = user_1, user_2 = user_2).exists():
		Friend.objects.filter(user_1 = user_1, user_2 = user_2)[0].delete()


	return redirect('friends')


def wallet_view(request):


	balance = Wallet.objects.filter(user = request.user)[0].balance
	transactions = Transaction.objects.filter(user_1 = request.user, status = True) | Transaction.objects.filter(user_2 = request.user, status = True)

	transactions_count = len(transactions)
	args = {
		'balance' : balance,
		'transactions' : transactions,
		'transactions_count' : transactions_count

	}
	return render(request, 'wallet.html', args)


def transactions_view(request):
	transactions = Transaction.objects.filter(user_1 = request.user, status = True) | Transaction.objects.filter(user_2 = request.user, status = True)

	transactions_count = len(transactions)
	args = {
		# 'balance' : balance,
		'transactions' : transactions,
		'transactions_count' : transactions_count
	}
	return render(request, 'transactions.html', args)

def add_money_view(request):
	args = {
	
	}

	if request.method == "POST":
		amount = request.POST.get('amount')
		print(amount)
		if int(amount) > 0 :
			wallet_instance = Wallet.objects.filter(user = request.user)[0]
			wallet_instance.balance = str(int(wallet_instance.balance) + int(amount))
			wallet_instance.save()

			return redirect('wallet')

	return render(request, 'add_money.html', args)

	
def transfer_money_view(request):

	friends = (Friend.objects.filter(user_1 = request.user) | Friend.objects.filter(user_2 = request.user) ) & Friend.objects.filter(status = True)

	if request.method == "POST":
		receiver_id = request.POST.get('u_id')
		amount = request.POST.get('amount')

		account_balance = Wallet.objects.filter(user = request.user)[0]

		if  int(account_balance.balance) - int(amount) >= 0: 

			account_balance.balance = int(account_balance.balance) - int(amount)
			account_balance.save()

			user_2 = Account.objects.filter(id = receiver_id)[0]
			t = Transaction(user_1 = request.user, user_2 = user_2, status = False, payment_method = 'paytm', amount = amount)
			
			t.save()
	
		return redirect('wallet')


	args = {
		'friends' : friends
	}
	return render(request, 'transfer_money.html', args)

def accept_decline_transaction_view(request):
	transaction_requests = Transaction.objects.filter(user_2 = request.user, status = False)

	transaction_requests_count = len(transaction_requests)

	args = {
		# 'balance' : balance,
		'transactions' : transaction_requests,
		'transactions_count' : transaction_requests_count
	}

	return render(request, 'accept_decline.html', args)

def accept_transaction_view(request, t_id):
	transaction = Transaction.objects.filter(id = t_id)[0]
	print(transaction.user_1)
	user_wallet = Wallet.objects.filter(user = request.user)[0]
	print(user_wallet)
	sender_wallet = Wallet.objects.filter(user = transaction.user_1)[0]
	print(sender_wallet.balance)
	transaction_amount = transaction.amount

	user_wallet.balance = user_wallet.balance + transaction_amount
	
	user_wallet.save()

	transaction.status = True
	transaction.save()

	return redirect('accept_decline')

def decline_transaction_view(request, t_id):
	transaction = Transaction.objects.filter(id = t_id)[0]
	sender_wallet = Wallet.objects.filter(user = transaction.user_1)[0]
	sender_wallet.balance = int(sender_wallet.balance) + int(transaction.amount)
	sender_wallet.save()
	transaction.delete()

	return redirect('accept_decline')


def messenger_view(request):
	args = {
	
	}	
	return render(request, 'add_money.html', args)

def create_group_view(request):
	args = {
	
	}	
	return render(request, 'add_money.html', args)

def create_post_view(request, u_id):

	
	args = {
		'u_id' : u_id
	}

	if request.method == "POST":
		content = request.POST.get('post_content')
		post_to = Account.objects.filter(id = u_id)[0]
		author = request.user
		print(content)
		print(post_to)
		print(author)
		f = feed(content = content, post_to = post_to, author = author)
		f.save()

		return redirect('/profile/'+str(u_id))


	return render(request, 'create_post.html', args)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = feed
    template_name = 'create_post.html'
    fields = ['content','post_to']
    success_url = reverse_lazy('home')
    login_url = "login"

    args = {

    }

    def get_form(self):
        form = super(PostCreateView, self).get_form()
        initial_base = self.get_initial() 
        # initial_base['menu'] = Menu.objects.get(id=1)
        form.initial = initial_base

        u = self.request.user
        friends = (Friend.objects.filter(user_1 = u) | Friend.objects.filter(user_2 = u) ) & Friend.objects.filter(status = True)
        print(friends.user_1)
        form.fields['post_to'].queryset = friends
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 
