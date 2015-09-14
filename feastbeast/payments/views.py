from django.shortcuts import render
from django.http import HttpResponse
import stripe
from carton.cart import Cart
from django.contrib.auth.models import User
from .models import UserPayment
import json
# Set your secret key: remember to change this to your live secret key in production
# See your keys here https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_Qt90eBDjHDIYHCO0YREdeEGk"



# Create your views here.
def charge(request):
	# Get the credit card details submitted by the form
	if request.is_ajax() or request.method == 'POST':

		if 'oldCard' in request.POST:  #using the card that is already saved

			#getting the stripe_id from UserPayment model
			customer_id = get_stripeid(request.user)

			#charging the customer
			try:
				stripe.charge.create(
					amount=amount,
					currency="aud",
					customer=customer_id

				)

			except stripe.error.CardError as e:
				# The card has been declined
				return HttpResponse("Charge Failed")

		else:

			token = request.POST['stripeToken']
			cart = Cart(request.session)
			amount = int(cart.total*100)

			#create a customer : todo : add checks
			customer = stripe.Customer.create(
							source=token,
							description="test description"
						)

			try:
				stripe.Charge.create(
				  amount=amount,
				  currency="aud",
				  customer=customer.id

				)

			except stripe.error.CardError as e:
				# The card has been declined
				return HttpResponse("Charge Failed")

			save_stripeid(request.user, customer.id)

			return HttpResponse("success")

	else:

		return HttpResponse("Illegal Post query")


#function to get the user cards
def getCards(request):
	try:
		user_payment_details = UserPayment.objects.get(user=request.user)
		customer = stripe.Customer.retrieve(user_payment_details.stripe_id)
		user_payment_methods = []
		default = ""
		for card_object in customer['sources']['data']:
			if(customer.default_source == card_object.id):
				default = card_object.id

			payment_method = {}
			payment_method['brand'] = card_object['brand']
			payment_method['last'] = card_object['last4']
			payment_method['card_id'] = card_object['id']
			user_payment_methods.append(payment_method)

		response = {'status' : 1, 'user_payment_methods' : user_payment_methods, 'default' : default}
	except UserPayment.DoesNotExist:
		response = {'status' : 0}
	return HttpResponse(json.dumps(response), content_type='application/json')

#Add a new card to the customer
def addCard(request):
	if request.is_ajax() or request.method == 'POST':
		stripe_id = UserPayment.objects.get(user=request.user).stripe_id
		token = request.POST['stripeToken']
		customer = stripe.Customer.retrieve(stripe_id)
		if 'id' not in customer:  # checking if the customer exists
			customer = stripe.Customer.create(
						source=token,
						description="test description"
					)

			save_stripeid(request.user, customer.id)

		card = customer.sources.create(source=token)
		response = {'status':1, 'brand': card.brand, 'last': card.last4, 'card_id': card.id }
		return HttpResponse(json.dumps(response), content_type='application/json')

#function to make the card default
def makeDefault(request):
	if request.is_ajax() or request.method == 'POST':
		stripe_id = UserPayment.objects.get(user=request.user).stripe_id
		customer = stripe.Customer.retrieve(stripe_id)
		customer.default_source = request.POST['card_id']
		customer.save()
		response = {'status' : 1}
	else:
		response = {'status' : 0}
	return HttpResponse(json.dumps(response), content_type='application/json')


#function to delete the card
def deleteCard(request):
	if request.is_ajax() or request.method == 'POST':
		current_user = UserPayment.objects.get(user=request.user)
		card_id = request.POST['card_id']
		customer = stripe.Customer.retrieve(current_user.stripe_id)
		customer.sources.retrieve(card_id).delete()
		default_card_id = stripe.Customer.retrieve(current_user.stripe_id).default_source
		if default_card_id is None: #all the cards have been deleted
			response = {'status' : 2}
		else:
			default_card = customer.sources.retrieve(default_card_id)
			response = {'status' : 1, 'brand' : default_card.brand, 'last' : default_card.last4, 'card_id' : default_card.id}
	else:
		response = {'status' : 0}
	return HttpResponse(json.dumps(response), content_type='application/json')


#method to save the stripe id of the current_user
def save_stripeid(user, stripe_id):
	current_user = User.objects.get(email=user.email)
	current_user_payment = UserPayment(user=current_user, stripe_id=stripe_id)
	current_user_payment.save()
	return

#method to retrieve the stripe id of the current_user
def get_stripeid(user):
	current_user = UserPayment.objects.get(user=user)
	return current_user.stripe_id


