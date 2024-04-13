Examples
=============

The best way to understand how this works, and what is useful for, it's probably with some examples, so here we go:

.. contents:: Table of Contents


CSV input format
----------------

The CSV should be just a simple file, with no headers, where each line represents an attribute of a table.

For example, take the following data:

.. list-table:: Table (recipes)
   :widths: 30 30 40
   :header-rows: 1

   * - recipe_id
     - name
     - ingredients
   * - 1
     - Chimichurri
     - | 1/2 Cup Oil
       | 2 tablespoons red wine vinegar
       | 1/2 cup finely chopped parsley
       | 1 tablespoon finely chopped chili
       | 1 teaspoon salt

The CSV that represents this table (`example1.csv <https://github.com/matteemol/dbSketcher/tree/main/examples/example1.csv>`_) would state

.. code-block:: python
    
    recipes, recipe_id, integer primary key
    recipes, name, text not null
    recipes, ingredients, text

As you can see, lines can be decomposed in three parameters each:

.. code-block:: python

  ``[TABLE NAME]`` = recipes
  ``[ATTRIBUTE NAME]`` = recipe_id
  ``[BASIC SQLITE DEFINITION]`` = integer primary key

  ``[TABLE NAME]`` = recipes
  ``[ATTRIBUTE NAME]`` = name
  ``[BASIC SQLITE DEFINITION]`` = text not null

  ``[TABLE NAME]`` = recipes
  ``[ATTRIBUTE NAME]`` = ingredients
  ``[BASIC SQLITE DEFINITION]`` = text

Then, after running in the terminal:

.. code-block:: python

  python dbsketcher/run.py example1.csv

We'll get two new output files:

* `example1.sql <https://github.com/matteemol/dbSketcher/tree/main/examples/example1.sql>`_

.. code-block:: python

  CREATE TABLE IF NOT EXISTS recipes (
  recipe_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  ingredients TEXT
  );

* `example1.uml <https://github.com/matteemol/dbSketcher/tree/main/examples/example1.uml>`_

.. code-block:: python

  @startuml

  left to right direction
  skinparam roundcorner 15
  skinparam shadowing true
  skinparam handwritten false
  skinparam class {
      BackgroundColor white
      ArrowColor #2688d4
      BorderColor #2688d4
  }

  !define table(x) entity x << (T, LightSkyBlue) >>
  !define primary_key(x) <b><color:#b8861b><&key></color> x</b>
  !define foreign_key(x) <color:#aaaaaa><&key></color> <u>x</u>
  !define column(x) <color:#efefef><&media-record></color> x
  !define column_fk(x) <color:#efefef><&media-record></color> <u>x</u>

  table( recipes ) {
    primary_key( recipe_id ): INTEGER PRIMARY KEY
    column( name ): TEXT NOT NULL
    column( ingredients ): TEXT
  }


  @enduml