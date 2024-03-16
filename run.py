import re, sys, csv
"""
table( formula ) {
  primary_key( formula_ID ): INTEGER PRIMARY KEY
  column( nombre ): TEXT NOT NULL
  column( cpnp ): TEXT NOT NULL
  foreign_key( clientId ): INTEGER <<FK>>
}
"""
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
    return tables


def csvToDict(file):

    tables = {}
    tableinfo = []
    updatedTable = []

    with open(file, newline='') as csvfile:
        tablereader = csv.reader(csvfile, delimiter=',')
# Ver para que no salga None en la ultima linea --------------------- <----------
        for row in tablereader:
            try:
                tableinfo = tables[row[0]]
            except:
                tables[row[0]] = tableinfo
            name = row[1].strip()
            col_type = row[2].strip()

            tableinfo.append((name, col_type))
            tables[row[0]] = tableinfo

            tableinfo = []
 
 
    print(tables)
    """
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
    return tables
"""

if __name__ == '__main__':
#    file = 'test.txt'
#    file = sys.argv[1]
#    print(umlToDict(file))
    file = 'tables.csv'
    print(csvToDict(file))
