Examples
=============

The best way to understand how this works, and what is useful for, it's probably with some examples, so here we go:

.. contents:: Table of Contents


CSV input format
----------------

The CSV should be just a simple file, with no headers, where each line represents an attribute of a table.

For example, take the following data:

Just 1 table
------------

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
       | (...)

The CSV that represents this table (`example1.csv <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example1.csv>`_) would state

.. code-block:: python
    
    recipes, recipe_id, integer primary key
    recipes, name, text not null
    recipes, ingredients, text

As you can see, each line is composed by three parameters:

| ``[TABLE NAME]`` = recipes
| ``[ATTRIBUTE NAME]`` = recipe_id
| ``[BASIC SQLITE DEFINITION]`` = integer primary key

| ``[TABLE NAME]`` = recipes
| ``[ATTRIBUTE NAME]`` = name
| ``[BASIC SQLITE DEFINITION]`` = text not null

| ``[TABLE NAME]`` = recipes
| ``[ATTRIBUTE NAME]`` = ingredients
| ``[BASIC SQLITE DEFINITION]`` = text

.. warning::
    Currently, the way to indicate that the attribute is a key, is:

    **Primary Key**: ``primary key``, ``primary_key``, ``pk``, ``pkey``

    **Foreign Key**: ``foreign key``, ``foreign_key``, ``fk``, ``fkey``

    Any other term used may rise to incorrect outputs (missing relationships)

Then, after running in the terminal:

.. code-block:: python

  python dbsketcher/run.py examples/example1.csv

We'll get two output files (and a `log <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example1.log>`_):

* `example1.sql <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example1.sql>`_

.. code-block:: python

  CREATE TABLE IF NOT EXISTS recipes (
  recipe_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  ingredients TEXT
  );

* `example1.uml <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example1.uml>`_

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

That renders to:

.. image:: images/example1.png
  :width: 280
  :alt: ERD example of 'Example 1' table

`See in PlantUML server <https://www.plantuml.com/plantuml/uml/ZP5HYzGm4CVVyob63kGAod6YHpbAkJifShYUibPmdvQqcRP3qsIP97IB-DrjkzIj--IKFkJ_dzzCClFWl6GVEYs4nig3jy1KDnuKCPQUh16k9NEGB3jW6umgBHjakFsmCbmZbUt9rE0vuCfef54za_Tee9BQhRrII-VWbu0ndcJPrdFvZrPRXhuXZxFpo6pxatZrxYwErViJO5aX_wl_5kALmeeCWfU5nkjZ16Wy-G6Ea2HmdR-1pVIux-tmf0D6aAP_YGDJ9tdOjpXCN5AaIJbLlxygulZkTZo-7gqqkPdL58x9JN6cAyj8jLde1PLpNA99I4SwdEbH3vrPWrXDtmXsg4Y-PImjgrNp2tHVjVzFd_kBqvY0iQG3EeYcRQmdiLXxKX3Tm_DBddtAjl1j-_pbSRk3pzbEm79xCBB3AIlFVkRmydNyVsmsAvzCpQW8ZNTBshGoyO16XKx_0G00>`_

Just 1 table with multiple items
--------------------------------

| Okay, that table it's kind of awful. Really, really unnormalized.
| A **sligthly** better version could be:

.. list-table:: Table (recipes)
   :widths: 30 30 40
   :header-rows: 1

   * - recipe_id
     - name
     - ingredient
   * - 1
     - Chimichurri
     - 1/2 Cup Oil
   * - 1
     - Chimichurri
     - 2 tablespoons red wine vinegar
   * - 1
     - Chimichurri
     - 1/2 cup finely chopped parsley
   * - 1
     - Chimichurri
     - 1 tablespoon finely chopped chili
   * - 1
     - Chimichurri
     - 1 teaspoon salt
   * - 1
     - Chimichurri
     - (...)

Since the information that the CSV file contains are the columns (attributes) names, the table to where they belong and the sql syntax that generates them, the **ONLY** difference in this file would be the name of the third column: as we now denormalized the table a little bit, we now have an entry (row) for each ingredient, so we changed ``ingredients`` by ``ingredient`` (without the last "s")

.. code-block:: python
    
    recipes, recipe_id, integer primary key
    recipes, name, text not null
    recipes, ingredient, text

So the other files would change in a similar way.

2 tables
--------

| If we go a little bit further in normalization, the first thing we should do, would be to split the recipe's name from the ingredients, right?

.. list-table:: Table 1 (recipes)
   :widths: 25 75
   :header-rows: 1

   * - recipe_id (primary_key)
     - name
   * - 1
     - Chimichurri

.. list-table:: Table 2 (ingredients)
   :widths: 25 55 20
   :header-rows: 1

   * - ingredient_id (primary_key)
     - ingredient
     - recipe_id (foreign_key)
   * - 1
     - 1/2 Cup Oil
     - 1
   * - 2
     - 2 tablespoons red wine vinegar
     - 1
   * - 3
     - 1/2 cup finely chopped parsley
     - 1
   * - 4
     - 1 tablespoon finely chopped chili
     - 1
   * - 5
     - 1 teaspoon salt
     - 1
   * - 6
     - (...)
     - (...)

Now the ``recipe_id`` attribute is not only the ``primary_key`` of the first table (**recipes**), but it's also the ``foreign_key`` of the second table (**ingredients**)

The CSV (`example3.csv <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example3.csv>`_) now does have some 'major' changes:

.. code-block:: python
    
    recipes, recipe_id, integer primary key
    recipes, name, text not null
    ingredients, ingredient_id, integer primary key
    ingredients, ingredient, text not null
    ingredients, recipe_id, integer foreign key (recipes)

And the ERD diagram (`example3.uml <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example3.uml>`_) is transformed to:

.. image:: images/example3.png
  :width: 657
  :alt: ERD example of 'Example 3' table

`See in PlantUML server <https://www.plantuml.com/plantuml/uml/ZP7HQzim4CRVzLVSA8m65ah7Le8nfkqmeophHkR1-XHawsmBor8uIpXcz7-VR8T4oLugumVVTx_lFf_kEyl9kbOnfh2qO0sGh6eBGX8MLXhDkaRg7IVU0XcdHM588y7jvq3eQYvCBtK5bXm6Gisrw4bQYnfAhhfGAnJlElZBm9z7NZJLPF_5A4FGrzBYf3mGcNukNdsyMwt4fnam993Eww-ClHDOIerWUQxmUhy0r5RQ0VOGnt2TVO3r-7E_ck5HELn0aXo97ScMqx1jS1YvE4_YOdIFhlBLwkxMVxxtKXBVJDK4zl5DVg9BGoWhVQGFA9_E9HgxnDFkHFkwQtK8OZa-7cnHIBuaB0o9OFW5kYsRDzF1V3Ql2QIko7UYjXqinXi9jn7AMobW4S7JSvP-JJVmS_Fq_M7p0j_I5mQ7A67xs9kbVp9u_k7Vt-irWxDDWKycTtZkobwFkMRv8bD8lYcFvYt-dyHFETX7qSbikKo2_A74s3rguLhr3m00>`_ (and the script's `output <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example3.log>`_)

Several tables
--------------

| If we go a little bit further in normalizing this scheme, we can break these tables a little bit more into:

.. list-table:: Table 1 (recipes)
   :widths: 25 50 25
   :header-rows: 1

   * - recipe_id (primary_key)
     - name
     - type_id (foreign_key)
   * - 1
     - Chimichurri
     - 2
   * - 2
     - Criolla
     - 2
   * - 3
     - Flan
     - 5

.. list-table:: Table 2 (recipe_type)
   :widths: 25 75
   :header-rows: 1

   * - type_id (primary_key)
     - type_name
   * - 1
     - Starter
   * - 2
     - Dressing
   * - 3
     - Main course
   * - 4
     - Side dish
   * - 5
     - Dessert

.. list-table:: Table 3 (recipe_ingredients)
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - recipe_id (foreign_key)
     - ingredient_id (foreign_key)
     - quantity
     - unit_of_measurement
     - preparation
   * - 1
     - 1
     - 1/2
     - Cup
     - 
   * - 1
     - 2
     - 2
     - tablespoons
     - 
   * - 1
     - 3
     - 1/2
     - Cup
     - Finely chopped

.. list-table:: Table 4 (ingredient_list)
   :widths: 20 80
   :header-rows: 1

   * - ingredient_id (primary_key)
     - ingredient_name
   * - 1
     - Sunflower Oil
   * - 2
     - Red wine vinegar
   * - 3
     - Parsley
   * - 4
     - Chili
   * - 5
     - Salt

To generate an ERD diagram, the input could be (`example4.csv <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example4.csv>`_):

.. code-block:: python

  recipes, recipe_id, integer primary key
  recipes, name, text
  recipes, type_id, integer foreign key (recipe_type)
  recipe_type, type_id, integer primary key
  recipe_type, type_name, text not null
  recipe_ingredients, recipe_id, integer foreign key (recipes)
  recipe_ingredients, ingredient_id, integer foreign key (ingredient_list)
  recipe_ingredients, quantity, real not null
  recipe_ingredients, unit_of_measurement, text not null
  recipe_ingredients, preparation, text
  ingredient_list, ingredient_id, integer primary key
  ingredient_list, ingredient_name, text not null

With this input, we get this `output <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example4.log>`_ and the ERD diagram (`example4.uml <https://github.com/matteemol/dbSketcher/tree/rtd-docs/examples/example4.uml>`_):

.. image:: images/example4.png
  :width: 759
  :alt: ERD example of 'Example 4' table

`See in PlantUML server <https://www.plantuml.com/plantuml/uml/ZPBHQzim4CRVzLVSA8m65ah7Le8nfka8eophHfR1-cGKwvo8s59saaZCwFy-AIQnwfaHXppuxllvEtsdUsCvMLTNZ5LOMh0QIAut5eGaBApKYfcjL3jEl0RIJeb2aqA2suzHmsouq7kfrc39OTJOS2Ns9Ar51IMlJDmhAcuC_67WdmTURDV7pt_IbIRORwJ5OsTAfFTjyUhztMGYFhI09e7qklx2s1k1fLG8bgygl3wC09MLje43f2bSBz_1F1pknxPvg1oE8ClEn8vapQd9jzW4BbrbQH6-dboj9fExM__wrhUozEPOpU2GtgmwkjI4SgrEz0dbnwUFfYxpjEjeNtUrYa4imy-3DGh9nuG-TH6Pzz2yt5vET_wiZGdyuiWhKTcyaiR2wBYLE95O8WMC4dXyMiu-pnRmVV7uTRfuXY-pPmQdayHonMiCm7BsQmbFt_p_vtpENixcX8NSOTuHflMFC-rKiNUd-V-CqLo_7MylXEykPjDvDr2dSKhQN9TvZTmumXgLZUVlotU4uJvRgTL9zk_fRBF3eLX3_Q90W_32ACsGKMXTQ1Mxn14FpnliU_SdILvlOZpE1hRSKx5MuSlTg8DWh61Hl4bYcpvcpaN6xb49LrT_0G00>`_