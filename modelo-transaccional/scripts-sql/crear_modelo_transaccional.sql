--- ==========================
--- CREAR MODELO TRANSACCIONAL
--- ==========================

--- El sig. script crea las tablas: cliente, pelicula, 
--- sala, asiento, funcion, boleto; en este orden.

--- Precaución!
--- Antes de correr, revisar si ya se tiene una conexión
--- con tablas que compartan nombre con las que se están
--- creando aquí.
--- Si es así, usar DROP TABLE y borrar esas tablas,
--- o bien, crear una nueva conexión a otra db limpia.

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
  "hora_inicio" timestamp NOT NULL,
  "hora_fin" timestamp NOT NULL,
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

--- ==========================
--- VERIFICACIONES ADICIONALES
--- ==========================

--- #1: No vender boletos para asientos ya ocupados.

--- índice único en boleto: id_funcion, num_asiento
CREATE UNIQUE INDEX ON "boleto" ("id_funcion", "num_asiento");
--- así, se evita que se vendan dos boletos
--- para la misma función y el mismo asiento

--- -----

--- #2: El boleto vendido tiene un asiento registrado.
--- 		¿Existe ese asiento en la sala de la proyección?

--- se define método validar_asiento_para_funcion()
--- para verificar que un asiento exista en la sala
--- de la función.
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
    SELECT 1 
		FROM asiento 
		WHERE id_sala = sala_funcion 
		AND num = NEW.num_asiento
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

--- ------------------

--- #3: En una sala de cine se pueden dar múltiples 
---     funciones,
--- 		pero estas funciones no pueden tener conflicto
---			de horario.

--- método verificar_conflicto_sala()
--- para revisar que no exista solapamiento de horarios
CREATE OR REPLACE FUNCTION verificar_conflicto_sala()
RETURNS TRIGGER AS $$
DECLARE
  conflicto RECORD;
BEGIN

	--- busca una función conflicto
	--- revisando las funciones que coincidan en la sala
	--- y revisando horarios
  SELECT 1 INTO conflicto
  FROM funcion
  WHERE id_sala = NEW.id_sala
    AND id != NEW.id  -- excluye la misma función si es UPDATE
    AND NOT (
      NEW.hora_fin <= hora_inicio OR
      NEW.hora_inicio >= hora_fin
    )
  LIMIT 1;

  IF FOUND THEN
    RAISE EXCEPTION 'La sala % ya tiene una función programada en ese horario.', NEW.id_sala;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--- hay trigger cada vez q se intente
--- insertar/actualizar función
CREATE TRIGGER trigger_verificar_conflicto_sala
BEFORE INSERT OR UPDATE ON funcion
FOR EACH ROW
EXECUTE FUNCTION verificar_conflicto_sala();
