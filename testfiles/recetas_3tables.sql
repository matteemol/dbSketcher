CREATE TABLE IF NOT EXISTS chefs (
 chef_Id INTEGER,
 nombre TEXT NOT NULL,
 apellido TEXT,
 apodo TEXT,
 paso TEXT,
 FOREIGN KEY (chef_Id)
  REFERENCES receta (chef_Id),
 FOREIGN KEY (paso)
  REFERENCES tipos (paso)
);

CREATE TABLE IF NOT EXISTS receta (
 receta_Id INTEGER PRIMARY KEY,
 nombre TEXT NOT NULL,
 tipo_Id INTEGER,
 origen TEXT,
 chef_Id INTEGER,
 ingredientes TEXT NOT NULL,
 puntaje REAL
);

CREATE TABLE IF NOT EXISTS tipos (
 tipo_Id INTEGER,
 paso TEXT NOT NULL,
 jerarquia TEXT,
 maridaje TEXT,
 FOREIGN KEY (tipo_Id)
  REFERENCES receta (tipo_Id)
);