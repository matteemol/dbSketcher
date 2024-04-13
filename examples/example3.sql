CREATE TABLE IF NOT EXISTS ingredients (
 ingredient_id INTEGER PRIMARY KEY,
 ingredient TEXT NOT NULL,
 recipe_id INTEGER,
 FOREIGN KEY (recipe_id)
  REFERENCES recipes (recipe_id)
    ON UPDATE SET NULL
    ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS recipes (
 recipe_id INTEGER PRIMARY KEY,
 name TEXT NOT NULL
);