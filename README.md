# dbSketcher

Tool to Sketch a db (plantUML ERD diagram + sqlite3 base code) out of a simple CSV file.

Test it live!:<br>
<a href="https://matteemol.eu.pythonanywhere.com" target="_blank">https://matteemol.eu.pythonanywhere.com</a>

## Why? and When?

When designing a database, you probably won't get to your final scheme on the first shot (if you do, then this program may be too basic for you).

While designing a db myself, I found it quite annoying to go back and forth with some attributes & tables, so dbSketcher was born.

## How?

Very, very easy. Write a simple CSV file (e.g. "my_sketch.csv") with just 3 columns (no headers), having some sqlite declarations in mind:

>    ``table_name``, ``attribute_name``, ``sqlite declaration``

Then run in the console:

>    ``python run.py my_sketch.csv``

And voilà! You'll obtain your own ``my_sketch.uml`` and ``my_sketch.sql`` with the UML and SQL code respectively, to sketch your db and visualize it easily right away! (and with the ``.sql`` script you can generate the basic database to start working)

## Documentation, help and Examples

Please visit <a href="https://dbsketcher.readthedocs.org" target="_blank">the official documentation in the Read The Docs site</a>

## Basic example

**Input**

CSV file:

``example3.csv``

>  recipes, recipe_id, integer primary key<br>
>  recipes, name, text not null<br>
>  ingredients, ingredient_id, integer primary key<br>
>  ingredients, ingredient, text not null<br>
>  ingredients, recipe_id, integer foreign key (recipes)<br>

**Output**

Terminal:

>  CSV to dict - Tables:<br>
>  {'ingredients': [('ingredient_id', 'pk', 'INTEGER PRIMARY KEY'), ('ingredient', 'col', 'TEXT NOT NULL'), ('recipe_id', 'fk (recipes)', 'INTEGER')], 'recipes': [('recipe_id', 'pk', 'INTEGER PRIMARY KEY'), ('name', 'col', 'TEXT NOT NULL')]}<br><br>
>  CSV to dict - Relationships (UML):<br>
>  {'recipe_id': [('recipes', 'ingredients')]}<br><br>
>  CSV to dict - Relationships (SQL):<br>
>  {'ingredients': [('recipe_id', 'recipes')]}<br>

SQL script:

``example3.sql``

>  CREATE TABLE IF NOT EXISTS ingredients (<br>
>   ingredient_id INTEGER PRIMARY KEY,<br>
>   ingredient TEXT NOT NULL,<br>
>   recipe_id INTEGER,<br>
>   FOREIGN KEY (recipe_id)<br>
>    REFERENCES recipes (recipe_id)<br>
>      ON UPDATE SET NULL<br>
>      ON DELETE SET NULL<br>
>  );<br>
>  <br>
>  CREATE TABLE IF NOT EXISTS recipes (<br>
>   recipe_id INTEGER PRIMARY KEY,<br>
>   name TEXT NOT NULL<br>
>  );<br>
