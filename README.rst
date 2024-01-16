
test go go
==========

.. image:: https://github.com/ikvk/test/blob/master/tux.png

Internal crossreference, like `example link`_.

How it works
==============

1. one

  ::

    https://github.com/ikvk

2. two

.. code-block:: python

    def a():
        a = b.encode('https://github.com')

3. three 2



Definition lists:

what
  Definition lists associate a term with
  a definition.

how
  The term is a one-line phrase, and the
  definition is one or more paragraphs


.. _`example link`:

end

тест 📧
=======

taram param


|shield_dm| |shield_ver| |shield_py| |shield_lec|

imap_tools 📧
=============

High level lib for work with email by IMAP:

- Basic message operations: fetch, uids, numbers
- Parsed email message attributes
- Query builder for search criteria
- Actions with emails: copy, delete, flag, move, append
- Actions with folders: list, set, get, create, exists, rename, subscribe, delete, status
- IDLE commands: start, poll, stop, wait
- Exceptions on failed IMAP operations
- No external dependencies, tested

.. |shield_dm| image:: https://img.shields.io/pypi/dm/imap_tools.svg
.. |shield_ver| image:: https://img.shields.io/pypi/v/imap_tools.svg
.. |shield_lec| image:: https://img.shields.io/pypi/l/imap_tools.svg
.. |shield_py| image:: https://img.shields.io/pypi/pyversions/imap_tools.svg

===============  ================================================================================================
Python version   3.5+
PyPI             https://pypi.python.org/pypi/imap_tools/
RFC              `IMAP4.1 <https://tools.ietf.org/html/rfc3501>`_,
                 `EMAIL <https://tools.ietf.org/html/rfc2822>`_,
                 `IMAP related RFCs <https://github.com/ikvk/imap_tools/blob/master/docs/IMAP_related_RFCs.txt>`_
Repo mirror      https://gitflic.ru/project/ikvk/imap-tools
===============  ================================================================================================

Installation
------------
::

    $ pip install imap-tools

