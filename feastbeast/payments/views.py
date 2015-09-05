from django.shortcuts import render
from django.http import HttpResponse
import stripe
from carton.cart import Cart

# Set your secret key: remember to change this to your live secret key in production
# See your keys here https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_Qt90eBDjHDIYHCO0YREdeEGk"



# Create your views here.
def charge(request):
	# Get the credit card details submitted by the form
	if request.is_ajax() or request.method == 'POST':
		token = request.POST['stripeToken']
		cart = Cart(request.session)
		amount = cart.total*100

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
		return HttpResponse("charege failed")

