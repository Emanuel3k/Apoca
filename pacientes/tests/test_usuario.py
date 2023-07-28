from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import User


def create_user(name):
    UserModel = get_user_model()
    if not UserModel.objects.filter(username=name).exists():
        user = UserModel.objects.create_user(name, password='gatopreto123')
        user.is_superuser = True
        user.is_staff = True
        user.is_assistente_social = True
        user.save()
        return user


class CustomUserTestCase(TestCase):
    '''
        attrs: descricao, usuario, cor
    '''

    def setUp(self):
        admin = create_user('Tobby')

    def test_user(self):
        usuario = User.objects.get(username='Tobby')
        self.assertEqual(str(usuario), 'Tobby')
