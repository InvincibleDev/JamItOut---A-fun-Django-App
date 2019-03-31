"""jamitout URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('login/', signIn,name="login"),
    path('logout/', signOut,name="logout"),
    path('signup/', signUp),
    path('', home),
    path('dashboard/', dashboard,name="dashboard"),
    path('create/', create_jam),
	path('readJam/<int:jam_id>/', read_jam, name="read"),
    path('displayJam/', display_jams),
    path('stopJam/<int:jam_id>/',stop_jam ),
    path('newline/',new_line),
    path('reopenJam/<int:jam_id>/',restartjam),
    path('oauthdone/',authdone),
    # path('sendemail/<str:jamline>/<str:jamname>/',email),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
