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

INSERT INTO pelicula (titulo, director, duracion, clasificacion_etaria, genero, sinopsis) VALUES
---enero 2024
('WONKA', 'Paul King', '01:56:00', 'ATP', 'Fantasía', 'Un joven Willy Wonka conoce a los Oompa Loompas y sueña con una fábrica.'),
('EL NIÑO Y LA GARZA', 'Hayao Miyazaki', '02:04:00', 'ATP', 'Animación', 'Un niño entra a un mundo mágico tras perder a su madre.'),
('POBRES CRIATURAS', 'Yorgos Lanthimos', '02:21:00', '+18', 'Drama', 'Una mujer revive con una nueva mente y redescubre el mundo.'),
('CON TODOS MENOS CONTIGO', 'Will Gluck', '01:44:00', '+13', 'Comedia romántica', 'Dos enemigos simulan ser pareja en una boda en Italia.'),
('WISH: EL PODER DE LOS DESEOS', 'Chris Buck', '01:35:00', 'ATP', 'Animación', 'Una joven enfrenta a un rey que controla los deseos.'),
---febrero
('KUNG FU PANDA 4', 'Mike Mitchell', '01:34:00', 'ATP', 'Animación', 'Po debe encontrar su sucesor mientras enfrenta un nuevo enemigo.'),
('DUNA: PARTE DOS', 'Denis Villeneuve', '02:46:00', '+13', 'Ciencia ficción', 'Paul Atreides se une a los Fremen para vengar a su familia.'),
('MADAME WEB', 'S.J. Clarkson', '01:56:00', '+13', 'Superhéroes', 'Una paramédica adquiere poderes de clarividencia al conectarse con una red de mujeres.'),
('BOB MARLEY: LA LEYENDA', 'Reinaldo Marcus Green', '01:47:00', 'ATP', 'Biográfico', 'La historia del ícono del reggae desde sus inicios hasta su legado.'),
('ANATOMIA DE UNA CAIDA', 'Justine Triet', '02:31:00', '+16', 'Drama judicial', 'Una escritora debe probar su inocencia tras la muerte de su esposo.'),
---marzo
('GHOSTBUSTERS: APOCALIPSIS FANTASMA', 'Gil Kenan', '01:55:00', 'ATP', 'Fantasía', 'La familia Spengler enfrenta una nueva amenaza sobrenatural en Nueva York.'),
('CABRINI', 'Alejandro Monteverde', '02:00:00', 'ATP', 'Biográfico', 'La historia de Francesca Cabrini y su lucha por los inmigrantes italianos en EE. UU.'),
('BAGHEAD: HABLA CON LOS MUERTOS', 'Alberto Corredor', '01:34:00', '+16', 'Terror', 'Una joven hereda un bar con un oscuro secreto en el sótano.'),
('GODZILLA Y KONG: EL NUEVO IMPERIO', 'Adam Wingard', '01:55:00', '+13', 'Acción', 'Godzilla y Kong deben unir fuerzas ante una nueva amenaza.'),
('IMAGINARIO: JUGUETE DIABÓLICO', 'Jeff Wadlow', '01:44:00', '+16', 'Terror', 'Una niña revive traumas a través de un oso de peluche poseído.'),
---abril
('PROFESIÓN PELIGRO', 'David Leitch', '02:05:00', '+13', 'Acción', 'Un doble de riesgo se ve envuelto en un caso criminal real.'),
('GUERRA CIVIL', 'Alex Garland', '01:49:00', '+16', 'Distopía', 'Fotoperiodistas atraviesan una EE.UU. dividida por un conflicto interno.'),
('ABIGAIL', 'Matt Bettinelli-Olpin', '01:49:00', '+16', 'Terror', 'Secuestran a una niña que resulta ser un ser sobrenatural.'),
('BACK TO BLACK', 'Sam Taylor-Johnson', '02:02:00', '+13', 'Biográfico', 'Relato íntimo de la vida de Amy Winehouse.'),
('UN GATO CON SUERTE', 'Ross Venokur', '01:38:00', 'ATP', 'Animación', 'Un gato maldito debe cambiar su destino con la ayuda de un niño.'),
---mayo
('GARFIELD: FUERA DE CASA', 'Mark Dindal', '01:41:00', 'ATP', 'Animación', 'Garfield se reencuentra con su padre y se une a un atraco de comida.'),
('EL PLANETA DE LOS SIMIOS: NUEVO REINO', 'Wes Ball', '02:25:00', '+13', 'Ciencia ficción', 'Un nuevo líder simio desafía el legado de César.'),
('FURIOSA: DE LA SAGA MAD MAX', 'George Miller', '02:28:00', '+16', 'Acción', 'Furiosa es secuestrada por un caudillo y lucha por sobrevivir.'),
('HACHIKO 2: SIEMPRE A TU LADO', 'Kenji Shimizu', '01:38:00', 'ATP', 'Drama', 'Una nueva historia inspirada en la fidelidad de un perro a su dueño.'),
('INMACULADA', 'Michael Mohan', '01:29:00', '+16', 'Terror', 'Una monja descubre oscuros secretos tras quedar embarazada en un convento.'),
---junio
('MI VILLANO FAVORITO 4', 'Chris Renaud', '01:35:00', 'ATP', 'Animación', 'Gru enfrenta un nuevo enemigo con ayuda de su hijo adoptivo.'),
('INTENSAMENTE 2', 'Kelsey Mann', '01:36:00', 'ATP', 'Animación', 'Riley ahora es adolescente y nuevas emociones llegan al cuartel.'),
('WINNIE THE POOH: MIEL Y SANGRE 2', 'Rhys Frake-Waterfield', '01:32:00', '+18', 'Terror', 'Winnie y sus amigos continúan su matanza en el Bosque de los Cien Acres.'),
('OBSERVADOS', 'Ishana Night Shyamalan', '01:42:00', '+13', 'Suspenso', 'Una joven queda atrapada en un bosque con criaturas que la observan.'),
('BAD BOYS: HASTA LA MUERTE', 'Adil & Bilall', '01:55:00', '+13', 'Acción', 'Mike y Marcus deben limpiar su nombre tras una conspiración interna.'),
---julio
('DEADPOOL Y WOLVERINE', 'Shawn Levy', '02:08:00', '+16', 'Superhéroes', 'Deadpool se une a Wolverine en una caótica aventura multiversal.'),
('MAXXXINE', 'Ti West', '01:45:00', '+18', 'Terror', 'Maxine busca la fama en Hollywood mientras el pasado la persigue.'),
('CORALINE 15 ANIVERSARIO', 'Henry Selick', '01:40:00', 'ATP', 'Animación', 'Una niña descubre un mundo alternativo con oscuros secretos.'),
('EL ÚLTIMO CONJURO', 'Michael Chaves', '01:52:00', '+16', 'Terror', 'Los Warren enfrentan su caso más peligroso: un demonio ancestral.'),
('TORNADOS', 'Lee Isaac Chung', '02:02:00', '+13', 'Acción', 'Una cazadora de tormentas lucha por sobrevivir a un brote de tornados.'),
---agosto
('LA TRAMPA', 'M. Night Shyamalan', '01:50:00', '+13', 'Thriller', 'Un músico queda atrapado en un evento que es en realidad una trampa.'),
('BORDERLANDS', 'Eli Roth', '01:47:00', '+16', 'Ciencia ficción', 'Un grupo de inadaptados busca un poder oculto en un planeta peligroso.'),
('ROMPER EL CÍRCULO', 'Zar Amir Ebrahimi', '01:38:00', '+13', 'Drama', 'Una joven lucha por escapar de un matrimonio forzado.'),
('ALIEN: ROMULUS', 'Fede Álvarez', '01:58:00', '+16', 'Terror', 'Un nuevo grupo de humanos enfrenta a un xenomorfo en una estación espacial.'),
('PULP FICTION 30 ANIVERSARIO', 'Quentin Tarantino', '02:34:00', '+18', 'Crimen', 'Historias entrelazadas de crimen y redención en Los Ángeles.'),
---septiembre
('BEETLEJUICE BEETLEJUICE', 'Tim Burton', '01:56:00', 'ATP', 'Fantasía', 'Beetlejuice regresa cuando una familia despierta al mundo de los muertos.'),
('TRANSFORMERS UNO', 'Josh Cooley', '01:45:00', 'ATP', 'Animación', 'Precuela sobre Optimus Prime y Megatron antes de la guerra.'),
('CAPITÁN AVISPA', 'Jonathan Meléndez', '01:30:00', 'ATP', 'Animación', 'Un superhéroe latino lucha por proteger a su colmena de villanos.'),
('LONGLEGS: COLECCIONISTA DE ALMAS', 'Osgood Perkins', '01:41:00', '+16', 'Terror', 'Una agente del FBI persigue a un asesino con conexiones ocultistas.'),
('EL CUERVO', 'Rupert Sanders', '01:57:00', '+16', 'Acción', 'Un músico resucita para vengar su muerte y la de su prometida.'),
---octubre
('ANORA', 'Sean Baker', '01:48:00', '+13', 'Drama', 'Una joven de Las Vegas se casa con un oligarca ruso, con consecuencias inesperadas.'),
('PESADILLA EN ELM STREET: 40 ANIVERSARIO', 'Wes Craven', '01:31:00', '+18', 'Terror', 'Freddy Krueger atormenta los sueños de adolescentes con una historia oscura.'),
('LA SUSTANCIA', 'Coralie Fargeat', '01:53:00', '+16', 'Ciencia ficción', 'Una sustancia permite alcanzar la perfección, pero a un alto precio.'),
('TERRIFIER 3', 'Damien Leone', '01:58:00', '+18', 'Terror', 'Art the Clown aterroriza un pueblo en vísperas de Navidad.'),
('VENOM: EL ÚLTIMO BAILE', 'Kelly Marcel', '02:00:00', '+13', 'Superhéroes', 'Eddie y Venom enfrentan su batalla final mientras son perseguidos.'),
---noviembre
('GLADIADOR 2', 'Ridley Scott', '02:40:00', '+16', 'Épico', 'Décadas después, el legado de Máximo inspira una nueva rebelión.'),
('EL CONDE DE MONTECRISTO', 'Alexandre de La Patellière', '02:18:00', '+13', 'Aventura', 'Edmond Dantès regresa con una nueva identidad para vengarse.'),
('WICKED', 'Jon M. Chu', '02:32:00', 'ATP', 'Musical', 'La historia no contada de la Bruja Mala del Oeste.'),
('MOANA 2', 'David G. Derrick Jr.', '01:38:00', 'ATP', 'Animación', 'Moana regresa para una nueva aventura más allá del océano.'),
('NO TE SUELTES', 'Bryan Bertino', '01:40:00', '+13', 'Terror', 'Una pareja queda atrapada en un juego de supervivencia en el bosque.');
---diciembre
('MUFASA: EL REY LEÓN', 'Barry Jenkins', '01:59:00', 'ATP', 'Animación', 'La historia jamás contada del ascenso de Mufasa como rey.'),
('EL TIEMPO QUE TENEMOS', 'Martín Cuevas', '01:47:00', '+13', 'Drama', 'Un hombre enfrenta su pasado tras recibir una noticia devastadora.'),
('KRAVEN: EL CAZADOR', 'J.C. Chandor', '01:38:00', '+16', 'Acción', 'Sergei Kravinoff busca demostrar que es el mayor cazador del mundo.'),
('SONIC 3: LA PELÍCULA', 'Jeff Fowler', '01:50:00', 'ATP', 'Aventura', 'Sonic y sus amigos enfrentan una nueva amenaza: Shadow.'),
('CÓDIGO: TRAJE ROJO', 'Anita Durán', '01:42:00', '+13', 'Thriller', 'Una agente secreta se infiltra en una red criminal bajo una identidad peligrosa.'),
---enero 2025
('PADDINGTON EN PERÚ', 'Dougal Wilson', '01:35:00', 'ATP', 'Comedia familiar', 'Paddington regresa a Perú con su familia Brown para visitar a su tía Lucy.'),
('MEDIUM', 'James Wan', '01:45:00', '+16', 'Terror', 'Una médium comienza a perder el control sobre los espíritus que invoca.'),
('BABYGIRL', 'Tina Gordon', '01:39:00', '+13', 'Drama', 'Una adolescente navega la maternidad inesperada y la búsqueda de identidad.'),
('INTERSTELLAR 10 ANIVERSARIO', 'Christopher Nolan', '02:49:00', '+13', 'Ciencia ficción', 'Reestreno del clásico de Nolan sobre viajes interestelares y relatividad.'),
('NOSFERATU', 'Robert Eggers', '01:55:00', '+16', 'Terror', 'Una reinterpretación oscura del vampiro clásico que acecha en la niebla.'),
---febrero
('FLOW', 'Karim Ainouz', '01:51:00', '+13', 'Drama', 'Un arquitecto se pierde en su viaje por el Amazonas buscando redención.'),
('CAPITÁN AMÉRICA: UN NUEVO MUNDO', 'Julius Onah', '02:10:00', '+13', 'Acción', 'Sam Wilson asume el escudo en una era de cambio e incertidumbre.'),
('CÓNCLAVE', 'Edward Berger', '01:40:00', '+13', 'Suspenso político', 'Un cardenal con un secreto es llamado al cónclave papal tras la muerte del Papa.'),
('EL BRUTALISTA', 'Brady Corbet', '02:03:00', '+16', 'Drama', 'La vida de un arquitecto marcado por su visión radical del diseño y la pérdida.'),
('UN COMPLETO DESCONOCIDO', 'Sofía Reyes', '01:43:00', '+13', 'Thriller psicológico', 'Una mujer descubre que su nuevo vecino no es quien dice ser.'),
---marzo
('BETTER MAN', 'Michael Gracey', '02:00:00', '+13', 'Musical biográfico', 'La historia de Robbie Williams y su ascenso en la música pop.'),
('EL MONO', 'Guillermo del Toro', '01:58:00', '+13', 'Fantasía oscura', 'Una criatura simbólica guía a un niño por sus miedos más profundos.'),
('MICKEY 17', 'Bong Joon-ho', '01:57:00', '+13', 'Ciencia ficción', 'Un clon desechable se rebela contra su destino en una misión espacial.'),
('BLANCA NIEVES', 'Marc Webb', '02:02:00', 'ATP', 'Fantasía musical', 'Nueva versión en acción real del clásico cuento con enfoque contemporáneo.'),
('IMPLACABLE', 'Pierre Morel', '01:41:00', '+16', 'Acción', 'Una agente busca venganza tras ser traicionada por su equipo.'),
---abril
('THUNDERBOLTS', 'Jake Schreier', '02:05:00', '+13', 'Acción', 'Un equipo de antihéroes liderado por Yelena Belova realiza misiones encubiertas.'),
('DROP: AMENAZA ANÓNIMA', 'Jorge Larraín', '01:44:00', '+13', 'Thriller', 'Una app de mensajería provoca una cadena de eventos catastróficos.'),
('UNTIL DAWN: NOCHE DE TERROR', 'David F. Sandberg', '01:49:00', '+16', 'Terror', 'Basada en el videojuego. Un grupo de jóvenes debe sobrevivir en la montaña.'),
('UNA PELÍCULA DE MINECRAFT', 'Jared Hess', '01:40:00', 'ATP', 'Aventura', 'Un niño debe salvar el mundo del Ender Dragon en el universo Minecraft.'),
('SMALL THINGS LIKE THESE', 'Tim Mielants', '01:43:00', '+13', 'Drama histórico', 'Un hombre descubre secretos oscuros de un convento en la Irlanda de los 80.').

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
    FOR j IN 1..300 LOOP
      INSERT INTO asiento(disponible)
      VALUES (TRUE);
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