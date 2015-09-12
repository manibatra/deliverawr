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
def get_cards(request):
	stripe_id = request.GET['stripe_id']
	customer = stripe.Customer.retrieve(stripe_id)
	user_payment_methods = []
	for card_object in customer['sources']['data']
		payment_method = {}
		payment_method['brand'] = card_object['brand']
		payment_method['last4'] = card_object['last4']
		user_payment_methods.append(payment_method)

	response = {'status' : 1, 'user_payment_methods' : user_payment_methods}
	return HttpResponse(json.dumps(response), content_type='application/json')

#Add a new card to the customer
def add_card(request):
	if request.is_ajax() or request.method == 'POST':
		stripe_id = request.POST['stripe_id']
		token = request.POST['stripeToken']
		customer = stripe.Customer.retrieve(stripe_id)
		card = customer.sources.create(source=token)
		response = {'status':1, 'brand': card.brand, 'last4': card.last4 }
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


