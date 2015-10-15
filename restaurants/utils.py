import requests
from django.conf import settings


#method to send the mail to the customer
def send_mail_deliverawr(text_to_send):
    return requests.post(
        settings.MAILGUN_URL + "/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Deliverawr <mailgun@" + settings.MAILGUN_DOMAIN + ">",
              "to": ["manibatra2002@gmail.com"],
              "subject": "Expression of Interest - Business",
              "text": text_to_send
	})