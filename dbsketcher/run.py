import re
import sys
import csv
import formatStrings


def identifyType(data: str)-> tuple:
    """
    Core function of the script. Reads the 3rd column of the CSV line
    (the so called ``SQL-type definition``) and breaks it down in 3:
    ``att_class``, ``col_type`` and -if exists- ``parent`` (only in case
    of foreign keys).

    :param ``data``: SQL-type attribute definition string.
    :type ``data``: String

    :return: 3 strings in a tuple.

        #. ``att_class``: the tag for the type of attribute:
        
           - **'col'** stands for "column", a standard non-key attribute
           - **'pk'** stands for "primary key"
           - **'fk (PARENT)'** stands for "foreign key", where PARENT
             is the table to which this key makes reference to.

        #. ``col_type``: SQLite code to declare an attribute (uppercase)
        #.  ``parent``: when the line corresponds to a foreign key, this
            output corresponds to the parent table's name.

    :rtype: tuple
    """

    att_class = "col"     
    col_type = data.upper()
    parent = ""
# Values initialized with the standard outputs for a plain column.

    pKeys = [' primary key', ' primary_key', ' pk', ' pkey']
# Lines in which the SQL-type definition: '... primary key',
# '... integer pk', or '... pkey' are broken down here, updating
# the att_class and col_type values (parent still == "")
    for key in pKeys:
        res = re.search(fr'{key}', data, re.IGNORECASE)
        if res != None:
            col_type = (
                data[:res.start()].upper()
                + data[res.end():].upper()
                + " PRIMARY KEY"
            )
            att_class = "pk"

    fKeys = [' foreign key', ' foreign_key', ' fk', ' fkey']
# Similar to the primary key lines, but for foreign keys. In addition,
# the parent string is updated according to the name between brackets
# after the 'fk' string in the CSV line.
    for key in fKeys:
        resKey = re.search(fr'{key}', data, re.IGNORECASE)
        resParent = re.search(r'[(\w]*[)]', data, re.IGNORECASE)
        if resKey != None:
            col_type = data[:resKey.start()].upper()
            parent = (
                data[(resParent.start() + 1):(resParent.end() - 1)].strip()
            )
            att_class = "fk" + f" ({parent})"

    return att_class, col_type, parent


def csvToDict(file)-> tuple:
    """
Starting point of the program. Takes a CSV file where each line contains:

    ``table name``, ``attribute``, ``SQL-type definition``

| and transforms this into a dictionary with the structure:
| {``TABLE NAME 1``:
  [(``ATTRIBUTE X``, ``ATTRIBUTE'S X TYPE``, ``SQL SCRIPT``), (...)]}        

If foreign keys are present, the CSV line should state the parent table
to which the foreign key refers, between brackets:

    i.e: ``SQL-type definition`` = 'integer foreign key (``PARENT TABLE``)'

If so, two additional dictionaries are populated by this function to
represent the relationships in a useful way for the rest of the code.

:param `file`: Each row of the file represents an attribute, the table
               where it belongs to, and eventually the parent (in case of
               a foreign key). The expected (correct) way to indicate this
               information is:
               
               ``table name``, ``attribute``, ``SQL-type definition``             
:type `file`: head-less CSV file

:return: 3 dictionaries as a 3-tuple. These dictionaries are

         - ``tables``:            tables and attributes information
        
        {``TABLE NAME 1``:
        [(``ATTRIBUTE X``, ``ATTRIBUTE'S X TYPE``, ``SQL SCRIPT``), (...)]}        
        
         - ``relationships_uml``: foreign key relationships, for UML output

        {``FOREIGN KEY``: [(``PARENT TABLE``, ``CHILD TABLE``)]

         - ``relationships_sql``: foreign key relationships, for SQL output

        {``CHILD TABLE``: [(``FOREIGN KEY``, ``PARENT TABLE``)]

:rtype: tuple
"""
    tables = {}
    relationships_uml = {}
    relationships_sql = {}

    tableinfo = []
    relinfo = []  #Aux list for relationships_uml
    families = [] #Aux list for relationships_sql

    with open(file, newline='') as csvfile:
        tablereader = csv.reader(csvfile, delimiter=',')
        for row in tablereader:
# Iterate over rows and add them to the returned dict.
# try/except used in case the line opened is the first appearance and
# the item in the dictionary doesn't exist. In such case, it's created.
            try:
                tableinfo = tables[row[0]]
            except:
                tables[row[0]] = tableinfo
            name = row[1].strip()
            att_class, col_type, parent = identifyType(row[2].strip())
# Breaks down the CSV line info into chunks that are then used to write
# the dictionary with an adequate format

            tableinfo.append((name, att_class, col_type))
            tables[row[0]] = tableinfo

            if parent != "":
# Relationships creation block. Analogue to the table creation block,
# whenever a fk is present, a parent-child relationship is created
# and stored in two dictionaries (although may seem redundant, it
# simplifies the functions' code from this point forward)
                try:
                    relinfo = relationships_uml[name]
                except:
                    relationships_uml[name] = relinfo

                relinfo.append((parent, row[0]))
                relationships_uml[name] = relinfo

                try:
                    families = relationships_sql[row[0]]
                except:
                    relationships_sql[row[0]] = families

                families.append((row[1].strip(), parent))
                relationships_sql[row[0]] = families

            relinfo = []
            tableinfo = []
            families = []
# All three auxiliary lists must be reinitialized between row and row

    return (
        dict(sorted(tables.items())),
        dict(sorted(relationships_uml.items())),
        dict(sorted(relationships_sql.items()))
    )


def dictToUml(tables:dict, relations:dict, fname:str)-> str:
    """
    Reads the dictionary of the table's information and generates a
    plantUML-ready file for it's visualization.

    :param `tables`: dictionary with the tables' data
    
            {``TABLE NAME 1``:
            [(``ATTRIBUTE X``, ``ATTRIBUTE'S X TYPE``, ``SQL SCRIPT``),
            (...)]}

    :type `tables`: Dictionary

    :param `relations`: if foreign keys are defined, this is the
            dictionary that holds the relationships information:
            
            {``ATTRIBUTE X``: [(``FATHER TABLE 1``, ``CHILD TABLE 1``)]}

    :type `relations`: Dictionary

    :param `fname`: name of the file with the CSV information (also
            used as the name for the output file)
    :type `fname`: String

    :return: UML script to sketch the database
    :rtype: String
    """

    umlScript = formatStrings.initUML
    references = {}
    references["pk"] = "primary_key( "
    references["fk "] = "foreign_key( "
    references["col"] = "column( "

    for table, columns in tables.items():
# Iterate over the {tables} dictionary to start composing the UML script
        colsLines = ""
        startLine = "table( " + table + " ) {\n"
        for col in columns:
            if col[0] in list(relations.keys()) and col[1][:2] == "fk":
# recognize if the attribute is a foreign key
                attLine = "  foreign_key( " + col[0] + " ): " + col[2] + "\n"
            else:
# if it's not foreign, then it's primary (Note: this conditional is
# testing the attributes that belong to the {relations} dictionary)
                attLine = (
                    "  "
                    + references[col[1].split("(")[0]] + col[0] + " ): "
                    + col[2] + "\n"
                )
            colsLines += attLine
        lastLine = "}"

        if table == list(tables.keys())[-1]:
# Detect if the table is the last one
            umlScript += (startLine + colsLines + lastLine)
        else:
            umlScript += (startLine + colsLines + lastLine + "\n\n")

    if relations != "":
# Trigger to detect if the tables are related and generate the links
        umlScript += "\n\n"
        for attribute, rel in relations.items():
            for family in rel:
                link = ""
                father, child = family
                link += (
                    father + "::" + attribute
                    + " --> "
                    + child + "::" + attribute
                )
                umlScript += link + "\n"

    umlScript += formatStrings.endUML
# Add the footer of the umlScript to make it ready for output

    with open(f"{fname[:-4]}.uml", "w") as uml_out:
        uml_out.write(umlScript)

    return umlScript


def dictToSql(tables:dict, relations:dict, fname:str)-> str:
    """
    Reads the dictionary of the table's information and generates an
    SQL script to create the tables with the references with minimal
    code.

    :param `tables`: dictionary with the tables' data

            {``TABLE NAME 1``:
            [(``ATTRIBUTE X``, ``ATTRIBUTE'S X TYPE``, ``SQL SCRIPT``),
            (...)]}

    :type `tables`: Dictionary

    :param `relations`: if foreign keys are defined, this is the
            dictionary that holds the relationships information:
            
            {``CHILD TABLE``: [(``ATTRIBUTE X``, ``FATHER TABLE 1``)]}

    :type `relations`: Dictionary

    :param `fname`: name of the file with the CSV information (also
            used as the name for the output file)
    :type `fname`: String

    :return: SQL script to generate the database with sqlite3
    :rtype: String
    """
    sqlScript = ""

    for table, columns in tables.items():
# Iterate over the {tables} dictionary to start composing the SQL script
        colsLines = ""
        startLine = "CREATE TABLE IF NOT EXISTS " + table + " (\n"

        for col in columns:

            if col != columns[-1]:
# This if/else is to consider (or not) the last colon before closing
# the SQL script
                attLine = " " + col[0] + " " + col[2] + ",\n"
            else:
                attLine = " " + col[0] + " " + col[2]
                try:
# This try/except evaluates if the attribute is a foreign key
                    for family in relations[table]:
                        link = ""
                        attLine += ",\n"
                        attribute, father = family
                        link += (
                            " FOREIGN KEY (" + attribute + ")\n  "
                            + "REFERENCES " + father + " (" + attribute + ")"
                            + formatStrings.fkSQL
# The standard action to be taken for foreign keys is read from the 
# formatStrings module
                        )
                        attLine += link
                except:
                    pass
            colsLines += attLine
        lastLine = "\n);"

        if table == list(tables.keys())[-1]:
# Detect if the table is the last one
            sqlScript += (startLine + colsLines + lastLine)
        else:
            sqlScript += (startLine + colsLines + lastLine + "\n\n")

    with open(f"{fname[:-4]}.sql", "w") as sql_out:
        sql_out.write(sqlScript)

    return sqlScript


def polishUML(raw_list: list)-> list:
    """
    Takes a list consisting of each of the UML text lines and
    transforms it into a list of tuples with the form (name, pk/fk/col,
    type), where type is the SQL script code to define the column's
    data type.

    :param raw_list: list of the database's attributes read from the
                    UML script.
    :type raw_list: list

    :return: list of tuples, where each tuple is composed by:

            (``ATTRIBUTE X``, ``ATTRIBUTE'S X TYPE``, ``SQL SCRIPT``)

    :rtype: list
    """

    clean = []
    att_class = ""
    name = ""
    col_type = ""

    for item in raw_list:
# Each item is a column of a certain table.
# First: identify if the column is something special (pk, fk) or
# just a plain column (attribute)

        pk = re.search(r"primary_key[( \w]*[ )]", item)
        fk = re.search(r"foreign_key[( \w]*[ )]", item)
        col = re.search(r"column[( \w]*[ )]", item)

# Then, select only the non-None values, and define the attribute type
# to be used in the returned tuples
        if pk != None: att_class = "pk"
        if fk != None: att_class = "fk"
        if col != None: att_class = "col"

# extract the name within the curved brackets
        name = item.split("(")[1].split(")")[0].strip()
# extract the data type of the column after the ":"
        col_type = item.split(":")[1].strip()

# generate the tuple and append it to the table's list
        clean.append((name, att_class, col_type))
    return clean


def umlToDict(file)-> dict:
    """
    Reads an UML script file and transforms it into a dictionary with
    the required format to be used to create a UML/SQL file.

    :param file: UML script file (see formatStrings for structure info)
    :type file: UML script

    :return: dictionary with the tables' data

            {``TABLE NAME 1``:
            [(``ATTRIBUTE X``, ``ATTRIBUTE'S X TYPE``, ``SQL SCRIPT``),
            (...)]}

    :rtype: dict
    """

    isWithin = False
    isTable = ""
    table = ""
    table_list = []
    tables = {}

    with open(file) as f:
        for line in f:
# Remove line breaking character from the read line
            line = line.rstrip()
# Search if the line contains the string "table (xxxxxxxxx)"
            isTable = re.search(r"table[( \w]*[ )]", line)
# If true, extract the table name from inside the ()
            if isTable != None:
                table = (isTable.string).split("(")[1].split(")")[0].strip()
# Start reading the table
                isWithin = True
            
            if isWithin:
# case: same line contains table name and first column:
# i.e: table (xxxx) { column 1: type
                if "{" in str(line):
                    column = line.split("{")[1].strip()
                else:
# analogue case, if the last column is the same line where the table ends
# i.e: column N: type }
                    if "}" in line:
                        column = line.split("}")[0].strip()
# Or just the -expected- case of a line with only the column info
                    else:
                        column = line.strip()
# if there's a match (a column exists in the line), then
# append it to the list of colums for the table
                if column != "": table_list.append(column)

#            print(table_list)
            if "}" in line:
                isWithin = False

# Each item of the list contains the name of the column, and 
# whether a column is a pk, fk or just a column. This func
# translates this into usable information.
                nice_list = polishUML(table_list)

# append the column list (with it's class & type) to a dictionary
# with "table name" : [columns] structure
                tables[table] = nice_list

# clear the table_list list to continue with the next table
                table_list = []
    return dict(sorted(tables.items()))


def polishSQL(raw_list: list)-> list:
    """
    Takes a list consisting of each of the SQL script lines and
    transforms it into a list of tuples with the form
    (name, pk/fk/col, type), where type is the SQL script code to
    define the column's data type.

    :param raw_list: list of the database's attributes read from the
                    SQL script.
    :type raw_list: list

    :return: list of tuples, where each tuple is composed by:

            (``ATTRIBUTE X``, ``ATTRIBUTE'S X TYPE``, ``SQL SCRIPT``)

    :rtype: list

    """

    clean = []
    att_class = ""
    name = ""
    col_type = ""

    for item in raw_list:
# Each item is a column of a certain table.
# First: identify if the column is something special (pk, fk) or
# just a plain column (attribute)

        pk = re.search(r"PRIMARY KEY", item)
        fk = re.search(r"<<FK>>", item)

# Then, select only the non-None values, and define the attribute type
# to be used in the returned tuples
        att_class = "col"
        if pk != None: att_class = "pk"
        if fk != None: att_class = "fk"

# extract the name within first two space characters
        name = item.split(" ", 1)[0].strip()
# extract the data type of the column after the second space character
        col_type = item.split(" ", 1)[1].strip()
        if col_type[-1] == ",": col_type = col_type[:(len(col_type)-1)]

# generate the tuple and append it to the table's list
        clean.append((name, att_class, col_type))
    return clean


def sqlToDict(file)-> dict:
    """
    Reads an SQL script file and transforms it into a dictionary with
    the required format to be used to create a UML/SQL file.

    :param file: SQL script file (minimum statements)
    :type file: sqlite3 script

    :return: dictionary with the tables' data

            {``TABLE NAME 1``:
            [(``ATTRIBUTE X``, ``ATTRIBUTE'S X TYPE``, ``SQL SCRIPT``),
            (...)]}

    :rtype: dict
    """

    isWithin = False
    isTable = ""
    table = ""
    table_list = []
    tables = {}

    with open(file) as f:
        for line in f:
            line = line.rstrip()
            isTable = re.search(r"CREATE TABLE", line)
            if isTable != None:
                table = (
                    (isTable.string).split("TABLE")[1]
                    .split("(")[0].strip()
                )
                isWithin = True
                
            if isWithin:
# This 'if' block is to consider all three cases of column appearances
# in the script:
# 1) CREATE TABLE xxxxx ( attribute...
# 2) attribute TEXT NOT NULL
# 3) attribute TEXT NOT NULL );
                if "(" in str(line):
                    column = line.split("(")[1].strip()
                else:
                    if ")" in line:
                        column = line.split(")")[0].strip()
                    else:
                        column = line.strip()

                if column != "": table_list.append(column)

            if ")" in line:
                isWithin = False

# Each item of the list contains the name of the column, and 
# whether a column is a pk, fk or just a column. This func
# translates this into usable information.
                nice_list = polishSQL(table_list)

# append the column list (with it's class & type) to a dictionary
# with "table name" : [columns] structure
                tables[table] = nice_list

# clear the table_list list to continue with the next table
                table_list = []
    return dict(sorted(tables.items()))


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Wrong number of arguments")
        print("python3 run.py <csv file>")
        exit()

    file = sys.argv[1]

    tables, relationships_uml, relationships_sql = csvToDict(file)

    output = "CSV to dict - Tables:\n" + \
    str(tables) + \
    "\nCSV to dict - Relationships (UML):\n" + \
    str(relationships_uml) + \
    "\nCSV to dict - Relationships (SQL):\n" + \
    str(relationships_sql)

    print("CSV to dict - Tables")
    print(tables)
    print("\nCSV to dict - Relationships (UML)")
    print(relationships_uml)
    print("\nCSV to dict - Relationships (SQL)")
    print(relationships_sql)

    with open(f"{file[:-4]}.log", "w") as logfile:
        logfile.write(output)

    dictToUml(tables, relationships_uml, file)
    dictToSql(tables, relationships_sql, file)
