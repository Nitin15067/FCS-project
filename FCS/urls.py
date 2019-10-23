"""FCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from account.views import (
	registration_view, 
	login_view, 
	logout_view
)

from dashboard.views import (
	dashboard_view,

    profile_view,
    edit_profile_info_view,
    change_password_view,

    friends_view,
    add_friend_view,

    search_view,

    wallet_view,
    add_money_view,
    transfer_money_view,
    transactions_view,

    messenger_view,
    create_group_view,
)

from home.views import (
	home_view
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^dashboard/$', dashboard_view, name = "dashboard"),
    
    url(r'^login/$', login_view, name="login"),
    url(r'^register/$', registration_view, name="register"),
    url(r'^logout/$', logout_view, name="logout"),


    url(r'^profile/edit/change_password/$', change_password_view, name="change_password"),
    url(r'^profile/edit/$', edit_profile_info_view, name="edit_profile_info"),
    url(r'^profile/(?P<u_id>\w+)/$', profile_view, name="profile"),
    url(r'^profile/(?P<u_id>\w+)/add_friend$', add_friend_view, name="add_friend"),



    url(r'^friends/$', friends_view, name="friends"),

    url(r'^search/$', search_view, name="search"),


    url(r'^messenger/create_group/$', create_group_view, name="create_group"),
    url(r'^messenger/$', messenger_view, name="messenger"),


    url(r'^wallet/add_money/$', add_money_view, name="add_money"),
    url(r'^wallet/transfer_money/$', transfer_money_view, name="transfer_money"),
    url(r'^wallet/transactions/$', transactions_view, name="transactions"),
    url(r'^wallet/$', wallet_view, name="wallet"),
    


    url(r'^$', home_view, name="home"),
]
