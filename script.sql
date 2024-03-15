CREATE TABLE hardware (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 price REAL NOT NULL
);

CREATE TABLE software (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 price REAL NOT NULL
);

table( formula ) {
  primary_key( formula_ID ): INTEGER PRIMARY KEY
  column( nombre ): TEXT NOT NULL
  column( cpnp ): TEXT NOT NULL
  foreign_key( clientId ): INTEGER <<FK>>
}

table( clientes ) {
  primary_key( client_ID ): INTEGER PRIMARY KEY
  column( nombre ): TEXT NOT NULL
  column( apellido ): TEXT NOT NULL
  column( razon_social ): TEXT NOT NULL
}

table( ingredientes ) {
  primary_key( clientId ): UUID 
  column( RazonSocial ): Character 
  column( Apodo ): Character
  column( NIF ): Character
  column( Direccion ): Character
  column( Mail ): email
  column( Telefono ): Character
}