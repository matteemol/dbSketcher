Examples
=============

Installation/Usage:
*******************
As the package has not been published on PyPi yet, it CANNOT be install using pip.

To run the program, execute the `python3 run.py <csv file>` command in the terminal. 

Input format
************
The starting point of the program is the ``csvToDict`` function 
.. code-block:: python

    def csvToDict(file)-> tuple:
    """
    Starting point of the program. Takes a CSV file with the structure:

    'table name', 'attribute', 'SQL-type definition'

    and transforms this into a dictionary with the structure:
    {'table name 1': [('attribute x', 'attribute x type', 'SQL script'),
                    (...)]}

    If foreign keys are present, the CSV line should state the parent table
    to which the foreign key refer, between brackets:

        i.e:`'SQL-type definition'` = 'integer foreign key ('parent table')

    If so, two additional dictionaries are populated by this function to
    represent the relationships in a useful way for the rest of the code.

    :param `file`: Base file without headers and only three columns
                'table name', 'attribute', 'SQL-type definition'             
    :type `file`: CSV file

    ...

    :return: 3 dictionaries as a 3-tuple. These dictionaries are

            `tables`:            tables and attributes information
            `relationships_uml`: foreign key relationships, for UML format
            `relationchips_sql`: foreign key relationships, for SQL format

    :rtype: tuple
    """
