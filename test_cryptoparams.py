# -*- coding: utf-8 -*-
import cryptoparams
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
