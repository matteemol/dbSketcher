Introduction
============

During the development of another project, I needed to transform some worksheets into a database, so I created **dbSketcher** as a simple program to help me design the database out from a CSV file with minimal code.

What it does
************

Takes a simple CSV input, consisting in three columns with the basic table/columns data, and generates an sqlite script (to create the tables) and a UML file with the ERD diagram for the data.
See some `Examples <examples.rst>`_

Limitations
***********

The code was developed just as an aid tool. **No unit tests were done**, and several errors can arise without explanation if the initial syntax of the CSV file is not properly done.

TODO List
*********

- Create a web interface to try the program


What it doesn't do (yet)
************************

- Work with mySQL or Postgresql (or anything that's not sqlite)
- Generate a sketch out of a complex db
- Read SQLAlchemy constructors
- Output SQLAlchemy base code
