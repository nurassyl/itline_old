from django.test import TestCase
from .models import Account
from django.core.exceptions import ValidationError

class AccountTestCase(TestCase):
	def test_normalize(self):
		account = Account()
		account.name = ' НҰРАСЫЛ АЛДАН НҰРҒАЗЫҰЛЫ '
		account.email = ' Nurassyl.Aldan@GMAIL.COM '
		account.password = ' 12345 '
		account.normalize()

		self.assertEqual(account.name, 'Нұрасыл Алдан Нұрғазыұлы')
		self.assertEqual(account.email, 'nurassyl.aldan@gmail.com')
		self.assertEqual(account.password, '12345')
	def test_validate(self):
		account = Account()
		account.name = 'Нұрасыл Алдан'
		account.email = 'nurassyl.aldan@gmail.com'
		account.password = '123456'
		account.language = 'kk'
		try:
			account.full_clean()
		except ValidationError as error:
			print(error)
