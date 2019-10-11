from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from dashboard.forms import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from account.models import Account

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


def profile_view(request):
	args = {
		'user': request.user
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
	args = {

	}
	return render(request, 'friends.html', args)

def wallet_view(request):
	args = {
	
	}
	return render(request, 'wallet.html', args)

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
