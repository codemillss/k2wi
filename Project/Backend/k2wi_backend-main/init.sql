/*kimchiData*/

CREATE SCHEMA k2wi_schema;

CREATE TABLE k2wi_schema.kimchi_info(
    kimchi_num int NOT NULL,
    kimchi_name text NOT NULL,
    PRIMARY KEY (kimchi_num)
);


CREATE TABLE k2wi_schema.recipe_order_image(
    kimchi_num int NOT NULL,
    recipe_order text NOT NULL,
    recipe_image_name text NOT NULL,
    recipe_image_path text NOT NULL,
    PRIMARY KEY (kimchi_num, recipe_order)
);

CREATE TABLE k2wi_schema.recipe_list(
    kimchi_num int NOT NULL,
    recipe_order int NOT NULL,
    recipe_detail text NOT NULL,
    PRIMARY KEY (kimchi_num, recipe_order),
    FOREIGN KEY (kimchi_num) REFERENCES k2wi_schema.kimchi_info(kimchi_num)
);

CREATE TABLE k2wi_schema.recipe_list_total(
    kimchi_num int NOT NULL,
    recipe_order int NOT NULL,
    recipe_detail text,
    PRIMARY KEY (kimchi_num, recipe_order),
    FOREIGN KEY (kimchi_num) REFERENCES k2wi_schema.kimchi_info(kimchi_num)
);

CREATE TABLE k2wi_schema.ingredients_list(
    kimchi_num int NOT NULL,
    kimchi_name text NOT NULL,
    ingredient text NOT NULL,
    PRIMARY KEY (kimchi_num),
    FOREIGN KEY (kimchi_num) REFERENCES k2wi_schema.kimchi_info(kimchi_num)
);

CREATE TABLE k2wi_schema.kimchi_image(
    kimchi_num int NOT NULL,
    recipe_order int NOT NULL,
    file_name text NOT NULL,
    file_path text NOT NULL,  -- ex: "/uploads/images/sample.jpg"
    PRIMARY KEY (kimchi_num),
    FOREIGN KEY (kimchi_num) REFERENCES k2wi_schema.kimchi_info(kimchi_num)
);


SELECT * FROM k2wi_schema.kimchi_info;

SELECT * FROM k2wi_schema.recipe_list WHERE recipe_order = 0;

SELECT * FROM k2wi_schema.ingredients_list;