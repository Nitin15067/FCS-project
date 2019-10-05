from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

def home_view(request):
	context = {
		"text" : "This is home view"
	}

	return render(request, 'home.html', context)

