CREATE TABLE "hechos_boletos" (
  "id" serial PRIMARY KEY,
  "num_asiento" integer,
  "id_pelicula" integer,
  "id_sala" integer,
  "id_cliente" integer,
  "hora_inicio_funcion" timestamp,
  "hora_fin_funcion" timestamp,
  "hora_compra" timestamp,
  "precio" integer,
  "genero" varchar,
  "clasificacion_etaria" varchar
);

CREATE TABLE "cliente" (
  "id" serial PRIMARY KEY,
  "nombres" varchar,
  "apellidos" varchar,
  "edad" integer
);

CREATE TABLE "sala" (
  "id" serial PRIMARY KEY,
  "tipo" varchar,
  "cant_asientos" integer
);

CREATE TABLE "pelicula" (
  "id" serial PRIMARY KEY,
  "titulo" varchar,
  "director" varchar,
  "duracion" time,
  "sinopsis" text
);

ALTER TABLE "hechos_boletos" ADD FOREIGN KEY ("id_cliente") REFERENCES "cliente" ("id");

ALTER TABLE "hechos_boletos" ADD FOREIGN KEY ("id_sala") REFERENCES "sala" ("id");

ALTER TABLE "hechos_boletos" ADD FOREIGN KEY ("id_pelicula") REFERENCES "pelicula" ("id");
