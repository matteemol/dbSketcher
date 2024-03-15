import re, sys
"""
table( formula ) {
  primary_key( formula_ID ): INTEGER PRIMARY KEY
  column( nombre ): TEXT NOT NULL
  column( cpnp ): TEXT NOT NULL
  foreign_key( clientId ): INTEGER <<FK>>
}
"""
def polish(raw_list: list):
    clean = []
    print(raw_list)

# First: identify the column type
    for item in raw_list:
        pk = re.search(r"primary_key[( \w]*[ )]", item)
        fk = re.search(r"foreign_key[( \w]*[ )]", item)
        col = re.search(r"column[( \w]*[ )]", item)

# select only the non-None values
        if pk != None: print(f"pk: {pk.string}")
        if fk != None: print(f"fk: {fk.string}")
        if col != None: print(f"col: {col.string}")

# If true, extract the table name from inside the ()
#            if table_line != None:
#                table = (table_line.string).split("(")[1].split(")")[0].strip()
#                print(f"Tabla '{table}':")

    clean = raw_list
    return clean

def umlToSql(file):

    isWithin = False
    tables = {}
    tableNum = 0
    table = ""
    table_line = ""
    table_list = []

    with open(file) as f:
        for line in f:
            # Remove line breaking character from the read line
            line = line.rstrip()
# Search if the line contains the string "table (xxxxxxxxx)"
            table_line = re.search(r"table[( \w]*[ )]", line)
# If true, extract the table name from inside the ()
            if table_line != None:
                table = (table_line.string).split("(")[1].split(")")[0].strip()
                print(f"Tabla '{table}':")
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
# if there's a match (a column exists in the line),
# append it to the list of colums for the table
                if column != "": table_list.append(column)

            if "}" in line:
                isWithin = False
# apply a similar algorithm to each table list to identify
# whether a column is a pk, fk or just a column, and it's name
                nice_list = polish(table_list)

# append the column list (with it's type) to a dictionary
# with "table name" : [columns] structure
                tables[table] = nice_list

# clear the table_list list to continue with the file
                table_list = []


if __name__ == '__main__':
    file = 'test.txt'
#    file = sys.argv[1]
    umlToSql(file)