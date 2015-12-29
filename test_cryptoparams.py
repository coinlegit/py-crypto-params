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
        self.assertTrue(cp is not None)

        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b")
        self.assertEqual("d0540d01397444a5f368185bfcb5b66b", cp.key)

        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        self.assertEqual("d0540d01397444a5f368185bfcb5b66b", cp.key)
        self.assertEqual("a1e1eb2a20241234a1e1eb2a20241234", cp.iv)

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "d0540d01397444a5f368185bfcb5b66b", "aieiebrazorf")

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "1-213", "a1e1eb2a20241234")

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "1-213")

    def test_simple(self):
        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        encrypted_string = cp.encrypt("aieiebrazorf")
        decrypted_string = cp.decrypt(encrypted_string)
        self.assertEqual("aieiebrazorf", decrypted_string)

    def test_complex_data(self):
        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        original_data = {
            "id": 1,
            "value": "aieie",
            "specs": {
                "sub_value": "brazorf"
            }
        }

        data_to_encrypt = json.dumps(original_data)
        encrypted_string = cp.encrypt(data_to_encrypt)
        decrypted_string = cp.decrypt(encrypted_string)
        decrypted_data = json.loads(decrypted_string)
        self.assertEqual(decrypted_data, original_data)

    def test_fairly_complex_data(self):
        cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")
        original_data = {
            "id": 1065412,
            "user_id": 657
        }

        data_to_encrypt = json.dumps(original_data)
        encrypted_string = cp.encrypt(data_to_encrypt)
        decrypted_string = cp.decrypt(encrypted_string)
        decrypted_data = json.loads(decrypted_string)
        self.assertEqual(decrypted_data, original_data)

    def test_properties(self):
        cp = cryptoparams.CryptoParams()
        cp.key = "d0540d01397444a5f368185bfcb5b66b"
        cp.iv = "a1e1eb2a20241234a1e1eb2a20241234"

        self.assertEqual(cp.key, "d0540d01397444a5f368185bfcb5b66b")
        self.assertEqual(cp.iv, "a1e1eb2a20241234a1e1eb2a20241234")

        try:
            cp.key = "aieie"
            self.fail("Wrong key accepted")
        except ValueError:
            pass

        try:
            cp.iv = "aieie"
            self.fail("Wrong initalization vector accepted")
        except ValueError:
            pass

        try:
            cp.key = dict()
            self.fail("Wrong key accepted")
        except ValueError:
            pass

        try:
            cp.key = "d0540d01397444a5f368185bfzb5b66b"
            self.fail("Wrong key accepted")
        except ValueError:
            pass

        try:
            cp.iv = tuple()
            self.fail("Wrong initalization vector accepted")
        except ValueError:
            pass

        try:
            cp.iv = "a1e1eb2a20241234a1e1eb2a2024z234"
            self.fail("Wrong initalization vector accepted")
        except ValueError:
            pass

    def test_wrong_parameters(self):
        cp = cryptoparams.CryptoParams()
        self.assertRaises(ValueError, cp.encrypt, dict())
        self.assertRaises(ValueError, cp.decrypt, dict())
