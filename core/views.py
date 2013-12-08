from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required
from paypalrestsdk import Payment

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
	restraunt = Restraunt.objects.get(pk=restraunt_id)
	reviews = Rating.objects.filter(restraunt=restraunt)
	average = 0
	for rating in reviews:
		average += rating.rating
	context['rating'] = average / float(len(reviews))
	context['foods'] = Food.objects.filter(restraunt=restraunt)[:6]
	context['restraunt'] = restraunt
	context['last_review'] = Rating.objects.filter(restraunt=restraunt)[:2]
	# rating = sum(reviews.rating) / float(len(reviews))
	current_line = Order.objects.filter(restraunt=restraunt).filter(status='Waiting')
	return render(request, 'core/restraunt.html', context)

def menu(request, restraunt_id):
	restraunt = Restraunt.objects.get(pk=restraunt_id)
	context = {'restraunt': restraunt}
	context['foods'] = Food.objects.filter(restraunt=restraunt)

	return render(request, 'core/menu.html', context)

def receipt(request, restraunt_id):
	context = {'user' : request.user}
	order = {}
	for food in Food.objects.filter(restraunt=restraunt_id):
		if int(request.POST['amount_' + str(food.id)]) > 0:
			print food
			print int(request.POST['amount_' + str(food.id)])
			order[food.id] = int(request.POST['amount_' + str(food.id)])

	return render(request, 'core/receipt.html', context)
