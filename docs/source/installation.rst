Installation
============

| As the package has not been published on PyPi yet, it CANNOT be install using pip.
| The repository can be found here: `https://github.com/matteemol/dbSketcher <https://github.com/matteemol/dbSketcher>`_
| Go ahead and `Fork me! <https://github.com/matteemol/dbSketcher/fork>`_

Usage
*****

To run the program, execute the ``python3 run.py <csv file>`` command in the terminal. 

| **Notes:**
  | - The ``python run.py <csv file>`` command should work too.

Input format
************

The CSV file should contain the following information per line:

``[TABLE NAME]``, ``[ATTRIBUTE NAME]``, ``[BASIC SQLITE DEFINITION]``

| Where ``[ATTRIBUTE NAME]`` and ``[TABLE NAME]`` are precisely that: the attribute's (column) name and the table where it belongs.
| The ``[BASIC SQLITE DEFINITION]`` is a little bit more tricky, but the tested values are:

- ``integer primary key``
- ``text`` / ``integer`` / ``real`` (optional: ``not null``)
- ``integer foreign key (PARENT_TABLE)``
