
#importing the django templete renderer
from django.template import loader, Context

#importing requests lib to send mail
import requests




#method to generate emailHTML
def generate_email_HTML(ver_key_url):
	context_dict = {}
	context_dict['ver_key_url'] = ver_key_url

	context = Context(context_dict)

	template = loader.get_template("users/confirm_signup.html")

	return template.render(context)


#method to send the mail to the customer
def send_confirmation_email(customer_email, emailHTML):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc0c1bcb688814d6c94674b7d42ca1018.mailgun.org/messages",
        auth=("api", "key-37d788bd314bf02a7fbb52dfe24efe4a"),
        data={"from": "Deliverawr <mailgun@sandboxc0c1bcb688814d6c94674b7d42ca1018.mailgun.org>",
              "to": [customer_email],
              "subject": "Confirm Email Address",
              "html": emailHTML
	})
