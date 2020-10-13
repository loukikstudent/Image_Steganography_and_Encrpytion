import unittest
from client_side_methods.emailv import validate_email
from client_side_methods.keygen import generate_keys
from client_side_methods.imagemanipulation import Image_Encryption, Image_Decryption, Image_Loader


class TestClientSide(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.key = generate_keys(24)
        cls.img_path = 't.jpg'

    def test_email_validation(self):
        correct_email = "loukikstudent@gmail.com"
        incorrect_email = "loukikstudent22@gmail.com"
        self.assertTrue(validate_email(correct_email))
        self.assertFalse(validate_email(incorrect_email))

    def test_encryption_and_decryption(self):
        loaded_image = Image_Loader(self.img_path)
        enc_img = Image_Encryption(self.img_path, self.key)
        self.assertNotEqual(loaded_image, enc_img)
        dec_img = Image_Decryption(enc_img, self.key, '', id="testing")
        self.assertEqual(dec_img, loaded_image)

