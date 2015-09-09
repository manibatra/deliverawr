from django.shortcuts import render
from django.http import HttpResponse
import stripe
from carton.cart import Cart
from django.contrib.auth.models import User
from .models import UserPayment

# Set your secret key: remember to change this to your live secret key in production
# See your keys here https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_Qt90eBDjHDIYHCO0YREdeEGk"



# Create your views here.
def charge(request):
	# Get the credit card details submitted by the form
	if request.is_ajax() or request.method == 'POST':

		if request.POST['oldCard'] == True:  #using the card that is already saved

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

			if request.POST['saveCard'] == True: #save the card and charge the customer
				#create a customer : todo : add checks
				customer = stripe.Customer.create(
								source=token,
								description=request.POST['card']['last4']
							)

				try:
					stripe.charge.create(
					  amount=amount,
					  currency="aud",
					  customer=customer.id

					)

				except stripe.error.CardError as e:
					# The card has been declined
					return HttpResponse("Charge Failed")

				save_stripeid(request.user, customer.id)

			else: #charge the card
				# Create the charge on Stripe's servers - this will charge the user's card
				try:
					charge = stripe.Charge.create(
						amount=amount, # amount in cents, again
						currency="aud",
						source=token,
						description=request.POST['description']
					)

				except stripe.error.CardError as e:
					# The card has been declined
					return HttpResponse("Charge Failed")

			return HttpResponse("Made a charge")

	else:
		return HttpResponse("Illegal Post query")

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


