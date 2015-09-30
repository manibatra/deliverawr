from django.test import TestCase
import json

# Create your tests here.
class UserSignupTests(TestCase):
	def test_validity_of_first_last_names(self):
		#check for smaller length
		response = self.client.post('/user/signup/', {'firstName' : 'M', 'lastName' : 'Batra'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)
		self.client.logout()
		response = self.client.post('/user/signup/', {'firstName' : 'Mani', 'lastName' : 'B'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)

		#check for longer length
		test_val = "x" * 31
		response = self.client.post('/user/signup/', {'firstName' : test_val, 'lastName' : 'Batra'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)
		self.client.logout()
		response = self.client.post('/user/signup/', {'firstName' : 'Mani', 'lastName' : test_val})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)

		#check for normal user signup
		response = self.client.post('/user/signup/', {'firstName' : 'Mani', 'lastName' : 'Batra', 'email' : 'manibatra@uq.net.au', 'password' : 'testpass' })
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 1)

	def test_validity_of_password(self):
		self.client.logout()
		#check for smaller password length
		response = self.client.post('/user/signup/', {'firstName' : 'Mani', 'lastName' : 'Batra', 'email' : 'manibatra@uq.net.au', 'password' : 'tef' })
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)

		#check for no password
		response = self.client.post('/user/signup/', {'firstName' : 'Mani', 'lastName' : 'Batra', 'email' : 'manibatra@uq.net.au'  })
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)

		response = self.client.post('/user/signup/', {'firstName' : 'Mani', 'lastName' : 'Batra', 'email' : 'manibatra@uq.net.au', 'password' : 'testpass' })
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 1)


#tests for user login
class UserLoginTests(TestCase):
	def setUp(self): #create a test user to test against
		response = self.client.post('/user/signup/', {'firstName' : 'Mani', 'lastName' : 'Batra', 'email' : 'manibatra@uq.net.au', 'password' : 'testpass' })
		self.client.logout()

	def test_validity_of_user_name(self):
		#checking invalid email
		response = self.client.post('/user/login/', {'emailLogIn' : 'M', 'passwordLogIn' : 'testpass'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)
		self.client.logout()

		#checking wrong email
		response = self.client.post('/user/login/', {'emailLogIn' : 'manibatra2002@gmail.com', 'passwordLogIn' : 'testpass'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)
		self.client.logout()

		#checking no email
		response = self.client.post('/user/login/', {'passwordLogIn' : 'testpass'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)
		self.client.logout()

		#checking correct email
		response = self.client.post('/user/login/', {'emailLogIn' : 'manibatra@uq.net.au', 'passwordLogIn' : 'testpass'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 1)
		self.client.logout()


	def test_validity_of_password(self):
		#checking invalid password
		response = self.client.post('/user/login/', {'emailLogIn' : 'manibatra@uq.net.au', 'passwordLogIn' : 'testp'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)
		self.client.logout()

		#checking wrong password
		response = self.client.post('/user/login/', {'emailLogIn' : 'manibatra@uq.net.au', 'passwordLogIn' : 'testpassing'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)
		self.client.logout()

		#checking no password
		response = self.client.post('/user/login/', {'emailLogIn' : 'manibatra@uq.net.au'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 0)
		self.client.logout()

		#checking correct password
		response = self.client.post('/user/login/', {'emailLogIn' : 'manibatra@uq.net.au', 'passwordLogIn' : 'testpass'})
		response = json.loads(response.content.decode('utf-8'))
		self.assertEqual(response['status'], 1)
		self.client.logout()
