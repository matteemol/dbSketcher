import re, sys, csv
import formatStrings

def polishUML(raw_list: list):
    """
Takes a list consisting of each of the UML text lines
and transforms it into a list of tuples with the form
(name, pk/fk/col, type), where type is the SQL script
code to define the column's data type
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
        
# If true, extract the table name from inside the ()
#            if table_line != None:
#                table = (table_line.string).split("(")[1].split(")")[0].strip()
#                print(f"Tabla '{table}':")

    return clean

def polishSQL(raw_list: list):
    """
Takes a list consisting of each of the SQL text lines
and transforms it into a list of tuples with the form
(name, pk/fk/col, type), where type is the SQL script
code to define the column's data type
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
        
# If true, extract the table name from inside the ()
#            if table_line != None:
#                table = (table_line.string).split("(")[1].split(")")[0].strip()
#                print(f"Tabla '{table}':")

    return clean


def umlToDict(file):

    isWithin = False
    table_line = ""
    table = ""
    table_list = []
    tables = {}

    with open(file) as f:
        for line in f:
# Remove line breaking character from the read line
            line = line.rstrip()
# Search if the line contains the string "table (xxxxxxxxx)"
            table_line = re.search(r"table[( \w]*[ )]", line)
# If true, extract the table name from inside the ()
            if table_line != None:
                table = (table_line.string).split("(")[1].split(")")[0].strip()
# Start reading the table
                isWithin = True
            
            if isWithin:
#                print(line)
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

def identifyType(data: str):
    att_class = "col"
    parent = ""
    col_type = data.upper()
    pKeys = [' primary key', ' pk', ' pkey']
    for key in pKeys:
        res = re.search(fr'{key}', data, re.IGNORECASE)
        if res != None:
            col_type = data[:res.start()].upper() + data[res.end():].upper() + " PRIMARY KEY"
            att_class = "pk"

    fKeys = [' foreign key', ' fk', ' fkey']
    for key in fKeys:
        resKey = re.search(fr'{key}', data, re.IGNORECASE)
        resParent = re.search(r'[(\w]*[)]', data, re.IGNORECASE)
        if resKey != None:
            col_type = data[:resKey.start()].upper()
            parent = data[(resParent.start() + 1):(resParent.end() - 1)].strip()
            att_class = "fk" + f" ({parent})"

    return att_class, col_type, parent


def csvToDict(file):

    tables = {}
    tableinfo = []
    relationships = {}
    relinfo = []

    with open(file, newline='') as csvfile:
        tablereader = csv.reader(csvfile, delimiter=',')
        for row in tablereader:
            try:
                tableinfo = tables[row[0]]
            except:
                tables[row[0]] = tableinfo
            name = row[1].strip()
            att_class, col_type, parent = identifyType(row[2].strip())

            tableinfo.append((name, att_class, col_type))
            tables[row[0]] = tableinfo

            if parent != "":
                try:
                    relinfo = relationships[name]
                except:
                    relationships[name] = relinfo

                relinfo.append((parent, row[0]))
                relationships[name] = relinfo

            relinfo = []
            tableinfo = []

    return dict(sorted(tables.items())), dict(sorted(relationships.items()))


def dictToSql(tables:dict):
    sqlScript = ""
    for table, columns in tables.items():
        colsLines = ""
        startLine = "CREATE TABLE " + table + " (\n"
        for col in columns:
            if col != columns[-1]:
                attLine = " " + col[0] + " " + col[2] + ",\n"
            else:
                attLine = " " + col[0] + " " + col[2] + "\n"
            colsLines += attLine
        lastLine = ");"

        if table != list(tables.keys())[-1]: sqlScript += (startLine + colsLines + lastLine + "\n\n")
        if table == list(tables.keys())[-1]: sqlScript += (startLine + colsLines + lastLine)

    with open("test_sql.sql", "w") as sql_out:
        sql_out.write(sqlScript)

    return sqlScript


def dictToUml(tables:dict, relations:dict, fname):
    umlScript = formatStrings.initUML
    references = {}
    references["pk"] = "primary_key( "
    references["fk "] = "foreign_key( "
    references["col"] = "column( "

    for table, columns in tables.items():
        colsLines = ""
        startLine = "table( " + table + " ) {\n"
        for col in columns:
            if col[0] in list(relations.keys()) and col[1][:2] != "fk":
                attLine = "  " + "column_fk( " + col[0] + " ): " + col[2] + "\n"
            else:
                attLine = "  " + references[col[1].split("(")[0]] + col[0] + " ): " + col[2] + "\n"
            colsLines += attLine
        lastLine = "}"

        if table != list(tables.keys())[-1]: umlScript += (startLine + colsLines + lastLine + "\n\n")
        if table == list(tables.keys())[-1]: umlScript += (startLine + colsLines + lastLine)

    if relations != "":
        umlScript += "\n\n"
        for attribute, rel in relations.items():
            for family in rel:
                link = ""
                father, child = family
                link += father + "::" + attribute + " --> " + child + "::" + attribute
                umlScript += link + "\n"

    umlScript += formatStrings.endUML

    with open(f"{fname}.uml", "w") as uml_out:
        uml_out.write(umlScript)

    return umlScript


def sqlToDict(file):

    isWithin = False
    table_line = ""
    table = ""
    table_list = []
    tables = {}

    with open(file) as f:
        for line in f:
# Remove line breaking character from the read line
            line = line.rstrip()
# Search if the line contains the string "table (xxxxxxxxx)"
            table_line = re.search(r"CREATE TABLE", line)
# If true, extract the table name from inside the ()
            if table_line != None:
                table = (table_line.string).split("TABLE")[1].split("(")[0].strip()
# Start reading the table
                isWithin = True
            
            if isWithin:
#                print(line)
# case: same line contains table name and first column:
# i.e: table (xxxx) { column 1: type
                if "(" in str(line):
                    column = line.split("(")[1].strip()
                else:
# analogue case, if the last column is the same line where the table ends
# i.e: column N: type }
                    if ")" in line:
                        column = line.split(")")[0].strip()
# Or just the -expected- case of a line with only the column info
                    else:
                        column = line.strip()
# if there's a match (a column exists in the line), then
# append it to the list of colums for the table
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
    file = 'recetas_2tables.csv'
#    file = sys.argv[1]
#    print("UML to dict")
#    print(umlToDict(file))
#    file = 'recetas_nonNF.csv'
    tables, relationships = csvToDict(file)
    print("\nCSV to dict - Tables")
    print(tables)
    print("\nCSV to dict - Relationships")
    print(relationships)

    dictToUml(tables, relationships, file)
    dictToSql(tables)
#    print(dictToSql(tables))
#    print("\nSql to dict")
#    file = "test_sql.sql"
#    print(sqlToDict(file))

# Acomodar lo de FK (hacer script de sql bien escrito)
# ver https://www.sqlitetutorial.net/sqlite-foreign-key/