# -*- coding: utf-8 -*-
import cryptoparams
import json
import logging
from unittest import TestCase


class TestCryptoParams(TestCase):
    """
        Unit test for :class:`cryptoparams.CryptoParams` class.
    """

    def setUp(self):
        logging.basicConfig(
                format="%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s",
                level=logging.DEBUG)

    def test_initialize(self):
        cp = cryptoparams.CryptoParams()
        self.assertIsNotNone(cp)

        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b")
        self.assertEqual("d0540d01397444a5f368185bfcb5b66b", cp.key)

        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        self.assertEqual("d0540d01397444a5f368185bfcb5b66b", cp.key)
        self.assertEqual("a1e1eb2a20241234a1e1eb2a20241234", cp.iv)

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "d0540d01397444a5f368185bfcb5b66b", "aieiebrazorf")

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "1-213", "a1e1eb2a20241234")

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "1-213")

    def test_encrypt(self):
        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        encrypted_string = cp.encrypt("aieiebrazorf")
        self.assertEqual(encrypted_string, "iW8qzzEWpWRN0NPNoOwu3A==")

    def test_encrypt_complex_data(self):
        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        data_to_encrypt = {
            "id": 1,
            "value": "aieie",
            "specs": {
                "sub_value": "brazorf"
            }
        }

        data_to_encrypt = json.dumps(data_to_encrypt)
        encrypted_string = cp.encrypt(data_to_encrypt)
        self.assertEqual(encrypted_string,
                         "kyQmwnZO9zQbn4PdxYRfvUhib+qGtZmxKBAY6HRL4DwZr2BGCPZ3XkJwdnQ1YFMJvFFnUQ9g+SUVM+nD0COrTA==")

    def test_encrypt_fairly_complex_data(self):
        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        data_to_encrypt = {
            "id": 1065412,
            "user_id": 657
        }

        data_to_encrypt = json.dumps(data_to_encrypt)
        encrypted_string = cp.encrypt(data_to_encrypt)
        self.assertEqual(encrypted_string,
                         "kyQ61TEGiGxTnZuLkt0d9NJtRuDAZzPfPUudLY8Hz5U=")

    def test_decrypt(self):
        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        encrypted_string = cp.decrypt("iW8qzzEWpWRN0NPNoOwu3A==")
        self.assertEqual(encrypted_string, "aieiebrazorf")

    def test_decrypt_complex_data(self):
        data_to_test = {
            "id": 1,
            "value": "aieie",
            "specs": {
                "sub_value": "brazorf"
            }
        }

        data_to_test = json.dumps(data_to_test)

        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        decrypted_string = cp.decrypt(
                "kyQmwnZO9zQbn4PdxYRfvUhib+qGtZmxKBAY6HRL4DwZr2BGCPZ3XkJwdnQ1YFMJvFFnUQ9g+SUVM+nD0COrTA==")
        self.assertEqual(data_to_test, decrypted_string)

    def test_decrypt_fairly_complex_data(self):
        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        data_to_test = {
            "id": 1065412,
            "user_id": 657
        }

        data_to_test = json.dumps(data_to_test)
        decrypted_string = cp.decrypt("kyQ61TEGiGxTnZuLkt0d9NJtRuDAZzPfPUudLY8Hz5U=")
        self.assertEqual(data_to_test, decrypted_string)
