CREATE TABLE IF NOT EXISTS ingredient_list (
 ingredient_id INTEGER PRIMARY KEY,
 ingredient_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipe_ingredients (
 recipe_id INTEGER,
 ingredient_id INTEGER,
 quantity REAL NOT NULL,
 unit_of_measurement TEXT NOT NULL,
 preparation TEXT,
 FOREIGN KEY (recipe_id)
  REFERENCES recipes (recipe_id)
    ON UPDATE SET NULL
    ON DELETE SET NULL,
 FOREIGN KEY (ingredient_id)
  REFERENCES ingredient_list (ingredient_id)
    ON UPDATE SET NULL
    ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS recipe_type (
 type_id INTEGER PRIMARY KEY,
 type_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipes (
 recipe_id INTEGER PRIMARY KEY,
 name TEXT,
 type_id INTEGER,
 FOREIGN KEY (type_id)
  REFERENCES recipe_type (type_id)
    ON UPDATE SET NULL
    ON DELETE SET NULL
);