# mando-sql-poc

🧠 Prototipo inicial de **mando.io**, una visión para hacer lo complejo natural.

## 🚀 ¿Qué es esto?

Este POC permite escribir una instrucción SQL como esta:

```sql
INSERT INTO dosage (medication_id, amount, date)
VALUES (5, 3, FROM '2025-04-01' TO '2025-04-05');
```
Y que se convierta automáticamente en:
```sql
INSERT INTO dosage (medication_id, amount, date) VALUES
(5, 3, '2025-04-01'),
(5, 3, '2025-04-02'),
(5, 3, '2025-04-03'),
(5, 3, '2025-04-04'),
(5, 3, '2025-04-05');
```

👉 Esta sintaxis puede simplificar cientos de líneas en sistemas de salud, educación o IoT, donde los datos periódicos son la norma.

---

✅ ¿Por qué?

Porque la repetición de fechas en SQL para insertar series de datos (medicación, sensores, clases, etc.) debería ser natural, no un castigo.

---

🧰 Uso por línea de comandos (CLI)

Este proyecto incluye un script CLI para expandir y ejecutar consultas SQL con rangos de fechas, con soporte para detección automática de tipos y columnas dinámicas.

Consulta la Guía CLI para más detalles sobre argumentos, ejecución y configuración de variables de entorno.

---

🆕 Novedades v2.0

* Detección automática de tipos básicos (INT, FLOAT, VARCHAR, BOOLEAN) según los valores en la query  
* Creación dinámica de tablas con columnas y tipos basados en la query de inserción  
* Expansión automática de rangos de fechas en la columna `date`  
* Mayor flexibilidad para insertar datos con tipos variados y múltiples columnas  

---

Desarrollado con visión por [@t-regexr](https://github.com/t-regexr)  
_A mi madre, visionaria en otra dimensión, que supo reconocer en mí un giro sin tornillo y creyó antes que yo._
