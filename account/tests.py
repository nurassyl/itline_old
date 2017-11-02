from django.test import TestCase
from .models import Account
from django.core.exceptions import ValidationError

class AccountTestCase(TestCase):
	def test_normalize(self):
		self.assertEqual(Account.normalize_name(' НҰРАСЫЛ АЛДАН НҰРҒАЗЫҰЛЫ '), 'Нұрасыл Алдан Нұрғазыұлы')
		self.assertEqual(Account.normalize_email(' Nurassyl.Aldan@GMAIL.COM '), 'nurassyl.aldan@gmail.com')
		self.assertEqual(Account.normalize_password(' 12345 '), '12345')
