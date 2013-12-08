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
	context['current_line'] = current_line
	return render(request, 'core/restraunt.html', context)

def menu(request, restraunt_id):
	restraunt = Restraunt.objects.get(pk=restraunt_id)
	context = {'restraunt': restraunt}
	context['foods'] = Food.objects.filter(restraunt=restraunt)

	return render(request, 'core/menu.html', context)

def receipt(request, restraunt_id):
	context = {'user' : request.user}
	order = {}
	total = 0
	for food in Food.objects.filter(restraunt=restraunt_id):
		if int(request.POST['amount_' + str(food.id)]) > 0:
			order[food.id] = (int(request.POST['amount_' + str(food.id)]), food.cost * int(request.POST['amount_' + str(food.id)])) 
			total = total + (food.cost * int(request.POST['amount_' + str(food.id)])
			)
	context['order'] = order
	for food in order:
		order_pending = Order(restraunt=Restraunt.objects.get(pk=restraunt_id), food=Food.objects.get(pk=food), user=request.user, status='Waiting', amount=order[food][0])
		order_pending.save()

	current_line = Order.objects.filter(restraunt=restraunt_id).filter(status='Waiting')
	context['current_line'] = current_line
	context['total'] = total
	context['oid'] = order_pending.id
	context['paypay_url'] = 'https://api.paypal.com/v1/payments/payment'
	return render(request, 'core/receipt.html', context)

def ebay(request):
	user = User.objects.get(pk=int(request.POST['uid']))
	order = Order.objects.get(pk=int(request.POST['oid']))
	total = float(request.POST['total'])
	payment = Payment({
	  "intent":  "sale",

	  # ###Payer
	  # A resource representing a Payer that funds a payment
	  # Payment Method as 'paypal'
	  "payer":  {
	    "payment_method":  "paypal" },

	  # ###Redirect URLs
	  "redirect_urls": {
	    "return_url": "http://localhost:8000/purchased/"+request.POST['oid']+"/"+request.POST['uid']+"/",
	    "cancel_url": "http://localhost:8000/" },

	  # ###Transaction
	  # A transaction defines the contract of a
	  # payment - what is the payment for and who
	  # is fulfilling it.
	  "transactions":  [ {

	    # ### ItemList
	    "item_list": {
	      "items": [{
	        "name": order.restraunt.name,
	        "sku": order.restraunt.name,
	        "price": str(total),
	        "currency": "USD",
	        "quantity": 1 }]},

	    # ###Amount
	    # Let's you specify a payment amount.
	    "amount":  {
	      "total":  total,
	      "currency":  "USD" },
	    "description":  "Food purchased at " + order.restraunt.name } ] } )

	if payment.create():
	  print("Payment[%s] created successfully"%(payment.id))
	  # Redirect the user to given approval url
	  for link in payment.links:
	    if link.method == "REDIRECT":
	      redirect_url = link.href
	      print("Redirect for approval: %s"%(redirect_url))
	else:
	  print("Error while creating payment:")
	  print(payment.error)
	context = {'user': request.user}
	context['order'] = order
	context['total'] = total
	current_line = Order.objects.filter(restraunt=order.restraunt.id).filter(status='Waiting')
	context['current_line'] = current_line
	return render(request, 'core/purchase.html', context)

def user_info(request):
	context = {'user' : request.user}
	context['user_info'] = UserExtension.objects.get(user=request.user)
	context['cc'] = "XXXX XXXX XXXX " + str(UserExtension.objects.get(user=request.user).card[:4]) 
	line = {}
	for order in Order.objects.filter(user=request.user).filter(status='Waiting'):
		line[order] = len(Order.objects.filter(restraunt=order.restraunt.id).filter(status='Waiting').filter(id__lte=order.id))
	context['lines'] = line

	current_line = Order.objects.filter(restraunt=order.restraunt.id).filter(status='Waiting')
	context['current_line'] = current_line
	return render(request, 'core/user_info.html', context)
