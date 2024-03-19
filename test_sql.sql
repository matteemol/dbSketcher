CREATE TABLE clientes (
 client_ID INTEGER PRIMARY KEY,
 nombre TEXT NOT NULL,
 apellido TEXT NOT NULL,
 razon_social TEXT NOT NULL
);

CREATE TABLE clientes_loc (
 client_ID INTEGER,
 nombre_loc TEXT NOT NULL,
 direccion TEXT NOT NULL,
 pais TEXT NOT NULL
);

CREATE TABLE formula (
 formula_ID INTEGER PRIMARY KEY,
 nombre TEXT NOT NULL,
 cpnp TEXT NOT NULL,
 client_ID INTEGER
);