from django.shortcuts import render, redirect
# from django.template import Context
from django.contrib.auth import login, authenticate
from account.forms import RegistrationForm, LoginForm
from account.models import Account


def dashboard_view(request):
	context = {
		"text" : "This is the dashboard"
	}

	accounts = Account.objects.all()
	context['accounts'] = accounts 

		# form = RegistrationForm()
		# context['registration_form'] = form
	return render(request, 'dashboard.html', context)

