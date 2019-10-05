from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, LoginForm

def registration_view(request):
	context = {}
	print("helre")
	if request.POST:
		form = RegistrationForm(request.POST)
		print(form)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('dashboard')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	print ("here")
	print (context)
	return render(request, 'register.html', context)


def login_view(request):
	context = {}

	user = request.user

	if user.is_authenticated:
		return redirect("dashboard")

	if request.POST:
		form = LoginForm(request.POST)
		print(form)
		print("validity")
		if form.is_valid():
			print("here")
			email = request.POST['email']
			password = request.POST['password']

			user = authenticate(email=email, password=password)

			if user :
				login(request, user)
				return redirect("dashboard")
	else:
		form = LoginForm()
	context['login_form'] = form
	return render(request, 'login.html', context)

def logout_view(request):
	print("here i am")
	logout(request)
	print ("loggin pout")
	return redirect('home')

