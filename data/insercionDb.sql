
--- 1. llenar 1500 clientes

DO $$
BEGIN
  FOR i IN 1..1500 LOOP
    INSERT INTO cliente (nombres, apellidos, edad)
    VALUES (
      'Nombre' || i,
      'Apellido' || i,
      FLOOR(RANDOM() * 52 + 18)::INTEGER  -- edad entre 18 y 70
    );
  END LOOP;
END $$;

--- 2. llenar peliculas

INSERT INTO pelicula (titulo) VALUES
---enero 2024
('WONKA'),
('EL NIÑO Y LA GARZA'),
('POBRES CRIATURAS'),
('CON TODOS MENOS CONTIGO'),
('WISH: EL PODER DE LOS DESEOS'),
---febrero
('KUNG FU PANDA 4'),
('DUNA: PARTE DOS'),
('MADAME WEB')
('BOB MARLEY: LA LEYENDA'),
('ANATOMIA DE UNA CAIDA'),
---marzo
('GHOSTBUSTERS APOCALIPSIS FANTASMA'),
('CABRINI'),
('BAGHEAD: HABLA CON LOS MUERTOS'),
('GODZILLA Y KONG: EL NUEVO IMPERIO'),
('IMAGINARIO: JUGUETE DIABOLICO'),
---abril
('PROFESION PELIGRO'),
('GUERRA CIVIL'),
('ABIGAIL'),
('BACK TO BLACK'),
('UN GATO CON SUERTE'),
---mayo
('GARFIELD: FUERA DE CASA'),
('EL PLANETA DE LOS SIMIOS NUEVO REINO'),
('FURIOSA: DE LA SAGA MAD MAX'),
('HACHIKO 2: SIEMPRE A TU LADO'),
('INMACULADA'),
---junio
('MI VILLANO FAVORITO 4'),
('INTENSAMENTE 2'),
('WINNIE THE POOH: MIEL Y SANGRE 2'),
('OBSERVADOS'),
('BAD BOYS: HASTA LA MUERTE'),
---julio
('DEADPOOL Y WOLVERINE'),
('MAXXXINE'),
('CORALINE 15 ANIVERSARIO'),
('EL ULTIMO CONJURO'),
('TORNADOS'),
---agosto
('LA TRAMPA'),
('BORDERLANDS'),
('ROMPER EL CIRCULO'),
('ALIEN ROMULUS'),
('PULP FICTION 30 ANIVERSARIO'),
---septiembre
('BEETLEJUICE BEETLEJUICE'),
('TRANSFORMERS UNO'),
('CAPITAN AVISPA'),
('LONGLEGS: COLECCIONISTA DE ALMAS'),
('EL CUERVO'),
---octubre
('ANORA'),
('PESADILLA EN ELM SREET: 40 ANIVERSARIO'),
('LA SUSTANCIA'),
('TERRIFIER 3'),
('VENOM: EL ULTIMO BAILE')
---noviembre
('GLADIADOR 2'),
('EL CONDE DE MONTECRISTO'),
('WICKED'),
('MOANA 2'),
('NO TE SUELTES'),
---diciembre
('MUFASA: EL REY LEON'),
('EL TIEMPO QUE TENEMOS'),
('KRAVEN: EL CAZADOR'),
('SONIC 3: LA PELICULA'),
('CODIGO: TRAJE ROJO'),
---enero 2025
('PADDINGTON EN PERU'),
('MEDIUM'),
('BABYGIRL'),
('INTERSTELLAR 10 ANIVERSARIO'),
('NOSFERATU'),
---febrero
('FLOW'),
('CAPITAN AMERICA: UN NUEVO MUNDO'),
('CONCLAVE'),
('EL BRUTALISTA'),
('UN COMPLETO DESCONOCIDO'),
---marzo
('BETTER MAN'),
('EL MONO'),
('MICKEY 17'),
('BLANCA NIEVES'),
('IMPLACABLE'),
---abril
('THUNDERBOLTS'),
('DROP: AMENAZA ANONIMA'),
('UNTIL DAWN: NOCHE DE TERROR'),
('UNA PELICULA DE MINECRAFT'),
('SMALL THINGS LIKE THESE');

--- 3. Insertar salas

INSERT INTO sala (tipo, n_asientos) VALUES
('NORMAL', 300),
('NORMAL', 300),
('IMAX', 300),
('NORMAL', 300),
('3D', 300);

--- 4. Insertar asientos

DO $$
BEGIN
  FOR i IN 1..5 LOOP
    FOR j in 1..300 LOOP
        INSERT INTO asiento(disponible)
            VALUES (
                1
            );
    END LOOP;
  END LOOP;
END $$;

/*
5. Por cada película, 10 funciones
que cada función tenga hora y salas únicas
A partir de ahí, insertar en tabla de hechos

*/

DO $$
DECLARE
  sala_id INT;
  fecha_proyeccion TIMESTAMP;
  boletos_vendidos INT;
  asiento_id INT;
  precio_funcion INT;
  cliente_id INT;
  hora_pago TIMESTAMP;
  pelicula_id INT;
BEGIN
  FOR x in 1..16 LOOP
  FOR i IN 1..5 LOOP
    fecha_proyeccion := TIMESTAMP '2024-01-02 14:30:00' + ((x-1) * INTERVAL '1 month');
    pelicula_id := i + 5 * (x-1);
    FOR j in 1..10 LOOP
        precio_funcion := FLOOR(RANDOM() * (5000-3000+1) + 3000);
        sala_id := FLOOR(RANDOM() * 5 + 1);
        asiento_id := 1 + 300 * (sala_id-1);
        boletos_vendidos := FLOOR(RANDOM() * (300-50+1) + 50);
        FOR k in 1..boletos_vendidos LOOP
            cliente_id := FLOOR(RANDOM() * 1500 + 1);
            hora_pago := fecha_proyeccion - (RANDOM() * INTERVAL '2 hours');
            INSERT INTO hechos_boletos
            (id_asiento, id_pelicula, id_sala, id_cliente, hora_funcion, hora_compra, precio)
            VALUES (
                asiento_id,
                pelicula_id,
                sala_id,
                cliente_id,
                fecha_proyeccion,
                hora_pago,
                precio_funcion
            );
            asiento_id := asiento_id + 1;
        END LOOP;
        fecha_proyeccion := fecha_proyeccion::date + TIME '14:30:00';
        fecha_proyeccion := fecha_proyeccion + INTERVAL '2 days' + (RANDOM() * INTERVAL '8 hours');
    END LOOP;
  END LOOP;
  END LOOP;
END $$;

--- Mostrando películas con los boletos que vendieron y su total recaudado
SELECT p.titulo, COUNT(*), SUM(precio) FROM hechos_boletos h
JOIN pelicula p ON h.id_pelicula = p.id
GROUP BY p.id;