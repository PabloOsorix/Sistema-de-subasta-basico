from app.utils.hasher import hash_sensible_data, check_hashed_data
from unittest import TestCase
import bcrypt


class TestPasswordHasher(TestCase):
    
    def setUp(self):
        self.plain_password = "contrasenaDeTesteo1"
    
    def test_password_hasher(self):
        hashed_password = hash_sensible_data(self.plain_password)
        print(hashed_password, "aqui")
        self.assertNotEqual(hashed_password, self.plain_password)
    
        # Verificar que la contraseña hasheada es válida al comparar con el texto plano
        self.assertTrue(bcrypt.checkpw(self.plain_password.encode('utf-8'), hashed_password.encode('utf-8')))
        self.assertIsInstance(hashed_password, str)
        
    def test_password_checker(self):
        hashed_password = hash_sensible_data(self.plain_password)
        self.assertTrue(check_hashed_data("contrasenaDeTesteo1", hashed_password))
        pass
