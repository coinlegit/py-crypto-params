import cryptoparams
import logging
import six
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

        cp = cryptoparams.CryptoParams("abcderfhoricsfd83ghxaqwdfhvx-213")
        self.assertEqual("abcderfhoricsfd83ghxaqwdfhvx-213", cp.key)

        cp = cryptoparams.CryptoParams("abcderfhoricsfd83ghxaqwdfhvx-213", "a1e1eb2a20241234")
        self.assertEqual("abcderfhoricsfd83ghxaqwdfhvx-213", cp.key)
        self.assertEqual("a1e1eb2a20241234", cp.iv)

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "abcderfhoricsfd83ghxaqwdfhvx-213", "aieiebrazorf")

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "1-213", "a1e1eb2a20241234")

        self.assertRaises(ValueError, cryptoparams.CryptoParams, "1-213")
