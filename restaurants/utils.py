import requests

#method to send the mail to the customer
def send_mail_deliverawr(text_to_send):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc0c1bcb688814d6c94674b7d42ca1018.mailgun.org/messages",
        auth=("api", "key-37d788bd314bf02a7fbb52dfe24efe4a"),
        data={"from": "Deliverawr <mailgun@sandboxc0c1bcb688814d6c94674b7d42ca1018.mailgun.org>",
              "to": ["manibatra2002@gmail.com"],
              "subject": "Thank you for ordering",
              "text": text_to_send
	})