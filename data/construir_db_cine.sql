CREATE TABLE "hechos_boletos" (
  "id" serial PRIMARY KEY,
  "id_asiento" integer,
  "id_pelicula" integer,
  "id_sala" integer,
  "id_cliente" integer,
  "hora_funcion" timestamp,
  "hora_compra" timestamp,
  "precio" integer
);

CREATE TABLE "cliente" (
  "id" serial PRIMARY KEY,
  "nombres" varchar,
  "apellidos" varchar,
  "edad" integer
);

CREATE TABLE "asiento" (
  "id" serial PRIMARY KEY,
  "disponible" boolean
);

CREATE TABLE "sala" (
  "id" serial PRIMARY KEY,
  "tipo" varchar,
  "n_asientos" integer
);

CREATE TABLE "pelicula" (
  "id" serial PRIMARY KEY,
  "titulo" varchar,
  "director" varchar,
  "duracion" timestamp,
  "clasificacion_etaria" varchar,
  "genero" varchar,
  "sinopsis" text
);

ALTER TABLE "hechos_boletos" ADD FOREIGN KEY ("id_cliente") REFERENCES "cliente" ("id");

ALTER TABLE "hechos_boletos" ADD FOREIGN KEY ("id_asiento") REFERENCES "asiento" ("id");

ALTER TABLE "hechos_boletos" ADD FOREIGN KEY ("id_sala") REFERENCES "sala" ("id");

ALTER TABLE "hechos_boletos" ADD FOREIGN KEY ("id_pelicula") REFERENCES "pelicula" ("id");
