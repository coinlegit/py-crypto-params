# -*- coding: utf-8 -*-
import binascii
import Crypto.Cipher
import Crypto.Hash.MD5
import Crypto.Random.random
import logging
import six
import string


class CryptoParams(object):
    """
        Provide encryption and decryption function for strings that use AES symmetric algorithm with CBC
            (which is compatible with `crypto-js <https://code.google.com/p/crypto-js/>`_).

        Padding implemented as per `RFC 2315 <http://www.ietf.org/rfc/rfc2315.txt>`: PKCS#7 page 21

        First base implementation for this class is taken from
            `marcoslin gist <https://gist.github.com/marcoslin/8026990>`_.

        :param str key: 32 bytes key used to initialize AES algorithm
        :param str iv: 16 bytes hexadecimal initialization vector used to initialize AES algorithm
        :raises ValueError: if parameters are incorrect
    """

    _BLOCK_SIZE_ = 16
    """
        AES Data block size
    """

    @property
    def key(self):
        """
            AES Key used by the class

            :return: 32 bytes Key used by the class
            :rtype: str
            :raises ValueError: if invalid key is provided
        """
        return binascii.b2a_hex(self._key)

    @key.setter
    def key(self, value):
        self._key = self._validate_key(value)

    @property
    def iv(self):
        """
            Initialization vector used by this class

            :return: 16 bytes initialization vector used by the class
            :rtype: str
            :raises ValueError: if invalid key is provided
        """
        return binascii.b2a_hex(self._iv)

    @iv.setter
    def iv(self, value):
        self._iv = self._validate_iv(value)

    def _pad_string(self, value):
        """
            Pad a string according to `PKCS#7 <http://www.ietf.org/rfc/rfc2315.txt>`_.

            :param str value: Value that need to be padded
            :return: padded string
            :rtype: str
            :raises ValueError: if parameter is incorrect
        """
        if not isinstance(value, six.string_types):
            six.reraise(ValueError, "Value should be a string")
        value_len = len(value)
        pad_size = self._BLOCK_SIZE_ - (value_len % self._BLOCK_SIZE_)
        return value.ljust(value_len + pad_size, chr(pad_size))

    def _unpad_string(self, value):
        """
            Unpad a string according to `PKCS#7 <http://www.ietf.org/rfc/rfc2315.txt>`_.

            :param str value: Value that need to be unpadded
            :return: unpadded string
            :rtype: str
            :raises ValueError: if parameter is incorrect
        """
        if not isinstance(value, six.string_types):
            six.reraise(ValueError, "Value should be a string")
        value_len = len(value)
        pad_size = ord(value[-1])
        if pad_size > self._BLOCK_SIZE_:
            six.reraise(ValueError, "Input is not padded or padding is corrupt")
        return value[:value_len - pad_size]

    def _generate_key(self):
        """
            Generate a random AES key using a secure randomizer algorithm

            :return: Random bytes used as AES Key (32 bytes)
            :rtype: str
        """
        randomic_sequence = ""
        base_dict = string.printable
        randomizer = Crypto.Random.random.StrongRandom()
        for i in range(0, self._BLOCK_SIZE_):
            randomic_sequence += base_dict[randomizer.randrange(0, len(base_dict) - 1)]

        md5 = Crypto.Hash.MD5.new(randomic_sequence)
        return binascii.a2b_hex(md5.hexdigest())

    def _generate_iv(self):
        """
            Generate a random initialization vector using a secure randomizer algorithm

            :return: Random bytes used as initialization vector (16 bytes)
            :rtype: binary
        """
        return Crypto.Random.get_random_bytes(self._BLOCK_SIZE_)

    @staticmethod
    def _validate_key(key):
        """
            Validate an AES key syntax (which means it states it if is a valid key from a syntax perspective,
            not if the key can decrypt an original text).

            Checks performed:

            * *key* must be a string
            * *key* must be 32 bytes

            :param str key: String used as key (please bear in mind that this **had not to be human readable**).

                It has to be exactly **32 bytes**
            :return: 32 bytes AES Key used for encryption
            :rtype: str
            :raises ValueError: it the key is unacceptable
        """
        if not isinstance(key, six.string_types):
            six.reraise(ValueError, "Key must be a string")
        if len(key) != 32:
            six.reraise(ValueError, "Key must be 32 bytes")
        try:
            return binascii.a2b_hex(key)
        except TypeError as e:
            six.reraise(ValueError, e)

    def _validate_iv(self, iv):
        """
            Validate an AES initialization vector.

            Checks performed:

            * *iv* must be a string
            * *iv* must be 16 bytes

            :param str iv: String used as initialization vector

                It has to be exactly **16 bytes**
            :return: 16 bytes initialization vector used for encryption
            :rtype: binary
            :raises ValueError: it the initialization vector is unacceptable
        """
        if not isinstance(iv, six.string_types):
            six.reraise(ValueError, "Initialization vector must be a string")
        if len(iv) != self._BLOCK_SIZE_:
            six.reraise(ValueError, "Initialization vector must be {bytes} bytes".format(bytes=self._BLOCK_SIZE_))
        try:
            return binascii.a2b_hex(iv)
        except TypeError as e:
            six.reraise(ValueError, e)

    def __init__(self, key=None, iv=None):
        """
            Initialize this class
        """
        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self._key = self._validate_key(key) if key is not None else self._generate_key()
        self._iv = self._validate_iv(iv) if iv is not None else self._generate_iv()

        self._logger.debug("CryptoParams initialization complete. AES Key: [{key}]. "
                           "Initialization vector: [{iv}].".format(key=self.key, iv=self.iv))


