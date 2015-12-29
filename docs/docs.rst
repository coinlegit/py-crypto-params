Documentation
=============

Installation
------------

This storage is hosted on `PyPI <https://pypi.python.org/pypi/py-crypto-params>`_. It can be easily installed
through *pip*:

.. code-block:: bash

   pip install py-crypto-params

Usage
-----

To initialize the encryption - decryption system, the :class:`CryptoParams <cryptoparams.CryptoParams>` class is used:

.. code-block:: python

  import cryptoparams

  cp = cryptoparams.CryptoParams()


The initialization without parameters auto generate a 32 bytes key and a 16 bytes initialization vector (as per
`AES <https://en.wikipedia.org/wiki/Advanced_Encryption_Standard>`_ specification).

The generated values are available through these properties:

- :func:`key <cryptoparams.CryptoParams.key>`
- :func:`iv <cryptoparams.CryptoParams.iv>`

:class:`CryptoParams <cryptoparams.CryptoParams>` class accept custom *key* and *initialization vector* though the
properties above and using the constructor:

.. code-block:: python

  import cryptoparams

  cp = cryptoparams.CryptoParams("d0540d01397444a5f368185bfcb5b66b", "a1e1eb2a20241234a1e1eb2a20241234")

The requisites to use custom *key* and *initialization vector* are:

- **key** must be a 32 bytes string written in hexadecimal base (it is not meant to be human readable)
- **initialization vector** must be a 16 bytes string written in hexadecimal base (it is not meant to be human readable)

If those requirements are not met a :class:`ValueError` exception will be raised.

Once the class has been initialized, a string could be encrypted using
:func:`encrypt(value) <cryptoparams.CryptoParams.encrypt>` method:

.. code-block:: python

  encrypted_data = cp.encrypt("aieiebrazorf")
  # encrypted_data contains "iW8qzzEWpWRN0NPNoOwu3A=="


This function returns a **Base64 encoded string** ready to be used into query strings.

To decrypt a **Base64 encoded string** with data the method used is
:func:`decrypt(value) <cryptoparams.CryptoParams.decrypt>`:

.. code-block:: python

  decrypted_data = cp.encrypt("iW8qzzEWpWRN0NPNoOwu3A==")
  # decrypted_data contains "aieiebrazorf"

It is possibile to encrypt and decrypt complex data transofming them into string such as *JSON*:

.. code-block:: python

    import cryptoparams
    import json

    original_data = {
        "id": 1065412,
        "user_id": 657
    }

    data_to_encrypt = json.dumps(original_data)
    encrypted_string = cp.encrypt(data_to_encrypt)
    decrypted_string = cp.decrypt(encrypted_string)
    decrypted_data = json.loads(decrypted_string)
    # decrypted_data contains a dict equal to original_data

Source and License
------------------

Source can be found on `GitHub <https://github.com/torre76/py-crypto-params>`_ with its included
`license <https://raw.githubusercontent.com/torre76/py-crypto-params/master/LICENSE.txt>`_.