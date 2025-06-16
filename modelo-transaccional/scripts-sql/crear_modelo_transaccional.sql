--- RECORDAR IMPORTANTE!
--- antes de ejecutar vaciar base de datos
--- de tablas que tengan los mismos nombres
--- tener cuidado también con los seriales
--- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

CREATE TABLE "cliente" (
  "id" serial PRIMARY KEY,
  "nombres" varchar,
  "apellidos" varchar,
  "edad" integer
);

CREATE TABLE "pelicula" (
  "id" serial PRIMARY KEY,
  "titulo" varchar NOT NULL,
  "director" varchar,
  "duracion" time,
  "clasificacion_etaria" varchar,
  "genero" varchar,
  "sinopsis" varchar
);

CREATE TABLE "sala" (
  "id" serial PRIMARY KEY,
  "tipo" varchar,
  "cant_asientos" int
);

CREATE TABLE "asiento" (
  "num" integer,
  "id_sala" integer,
  PRIMARY KEY ("id_sala", "num"),
  FOREIGN KEY ("id_sala") REFERENCES "sala" ("id")
);
--- omití el tipo de asiento

CREATE TABLE "funcion" (
  "id" serial PRIMARY KEY,
  "id_sala" integer,
  "id_pelicula" integer,
  "hora_funcion" timestamp NOT NULL,
  FOREIGN KEY ("id_sala") REFERENCES "sala" ("id"),
  FOREIGN KEY ("id_pelicula") REFERENCES "pelicula" ("id")
);

CREATE TABLE "boleto" (
  "id" serial PRIMARY KEY,
  "id_cliente" integer,
  FOREIGN KEY ("id_cliente") REFERENCES "cliente" ("id"),
  "id_funcion" integer,
  FOREIGN KEY ("id_funcion") REFERENCES "funcion" ("id"),
  "num_asiento" integer NOT NULL,
  "precio" integer NOT NULL,
  "hora_compra" timestamp
);

CREATE UNIQUE INDEX ON "boleto" ("id_funcion", "num_asiento");
--- así, dada una misma función,
--- no se venden dos o más boletos para el mismo asiento

--- función de validación con trigger
CREATE OR REPLACE FUNCTION validar_asiento_para_funcion()
RETURNS trigger AS $$
DECLARE
  sala_funcion integer;
BEGIN
  SELECT id_sala INTO sala_funcion FROM funcion WHERE id = NEW.id_funcion;
	--- obtiene la sala de la función del boleto insertado/actualizado
	--- y guarda el número en variable integer sala_funcion

  IF NOT EXISTS (
  	--- revisa si existe al menos un asiento (1)
  	--- tal que su sala corresponda a sala_funcion
    SELECT 1 FROM asiento WHERE id_sala = sala_funcion AND num = NEW.num_asiento
  ) THEN
  	--- si no existe, arroja la excepción
    RAISE EXCEPTION 'El asiento % no existe en la sala asociada a la función %', NEW.num_asiento, NEW.id_funcion;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
--- todo esto también se podría hacer en el script .py
--- o mejor, hacer con python que la excepción se vea en el menú
--- cuando falle la inserción por este trigger


--- trigger para que cada vez que se inserte un boleto
--- o que se actualice, verifique con validar_asiento_para_funcion()
CREATE TRIGGER trigger_validar_asiento
BEFORE INSERT OR UPDATE ON boleto
FOR EACH ROW EXECUTE FUNCTION validar_asiento_para_funcion();

