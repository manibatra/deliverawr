# Deliverawr

### A complete ordering system for restaurants

#### Various Components : 
- Landing Page
- Order Placement System
- Payment System
- User Registeration System

#### Languages Used : 
- Python
- HTML
- CSS
- Javascript

#### Framkeworks Used : 
- Django
- Stripe
- Django-Storages
- Raven
- PostgresSQL
- Docker

#### Services Used :
- Mailchimp : Mail (Order Confirmation, User Validation, Etc)
- Sentry : Error handnling and managment
- Twilio : SMS 
- HeapAnalytics : Anaytics

#### Hosted on : 
- Website : Heroku
- Static Media : AWS-S3

## How to Install 

1. Grab a copy of the project : 

```
git clone https://github.com/manibatra/deliverawr.git
```
2. Create a virtual environment and install dependencies
```
mkvirtualenv derliverawr_env
pip install -r requirements.txt
```
3. Update the database and S3 settings in `settings.py`.
4. Update the envrioment variables requiired in `settings.py`.
5. Initialize your database : 
```
python ./manage.py makemigrations
python ./manage.py migrate
```
6. Run the developement server to verify everything is working
```
python ./manage.py runserver
```


<div style="text-align:center"><img src="http://i.imgur.com/Dew7NwG.png" width="500"></div>
