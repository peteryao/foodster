from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required

from core.models import UserExtension
from order.models import Restraunt, Food, Order, Rating

def index(request):
	context = {'user': request.user}
	restraunts = Restraunt.objects.all()
	foods = []
	for restraunt in restraunts:
		foods.append(Food.objects.filter(restraunt=restraunt).latest('id'))
	context['restraunts'] = zip(restraunts, foods)
	return render(request, 'core/index.html', context)

def restraunt(request, restraunt_id):
	context = {'user' : request.user}
	
	return render(request, 'core/restraunt.html', context)