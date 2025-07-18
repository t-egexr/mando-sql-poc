# Propuesta de sintaxis SQL para inserciones con rangos de fechas

## Contexto

Trabajo mucho con datos diarios, especialmente en el área de salud, donde registro dosis de medicación y otros datos que ocurren en rangos de fechas continuos. Actualmente, insertar estos datos en bases de datos SQL requiere escribir muchas filas manualmente o usar scripts externos que generen las sentencias INSERT, lo que vuelve el proceso tedioso, propenso a errores y poco legible.

---

## Mi propuesta

Crear una sintaxis que permita hacer algo así:

```sql
INSERT INTO dosage (medication_id, amount, date)
VALUES (5, 3, FROM '2025-04-01' TO '2025-04-30');
```

Y que el motor SQL internamente lo expanda a múltiples filas, una por cada fecha en el rango, evitando la repetición manual.

## Beneficios

- Reduce la cantidad de líneas y complejidad en los scripts SQL.
- Facilita la productividad y la legibilidad del código.
- Evita la necesidad de herramientas externas para tareas comunes.
- Muy útil en áreas como salud, educación, IoT y otras que manejan datos periódicos.

## El intercambio con el equipo PostgreSQL

Envié esta idea al equipo de desarrollo de PostgreSQL, donde Álvaro Herrera — uno de los miembros del core — me respondió explicando que ya es posible hacer algo similar con generate_series(), un método muy poderoso pero menos accesible para desarrolladores no expertos en SQL.

Por ejemplo:

```
INSERT INTO dosage (medication_id, amount, date)
SELECT 5, 3, g
FROM generate_series(date '2025-04-01', '2025-04-30', '1 day') AS g;
```

Le respondí que la intención no era reemplazar esa función, sino ofrecer una sintaxis más natural y declarativa para quienes no están familiarizados con esa herramienta, haciendo el lenguaje SQL más ergonómico y amigable.

## El prototipo (POC)

Para probar la idea, desarrollé un prototipo en Python que transforma la sintaxis propuesta en múltiples sentencias INSERT explícitas, y lo integré con MySQL para demostrar su funcionamiento.

Este proyecto está disponible aquí:

[Mando SQL POC](https://github.com/t-regexr/mando-sql-poc)

## Reflexión final

Me apasiona simplificar flujos complejos con hacks inteligentes. Este pequeño experimento nació de una necesidad real y hoy es una invitación abierta a imaginar lenguajes más naturales, accesibles y potentes para todos.

## Créditos

Desarrollado por Tyrannosaurus RegExr (@t-regexr) — Evolucionando código desde lo prehistórico a lo natural.

*“Nunca se desea ardientemente lo que solo se desea por razón” — F. Alexandre*
