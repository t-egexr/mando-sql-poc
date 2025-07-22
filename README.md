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
![Made with ❤️ and Python](https://img.shields.io/badge/built%20with-Python-blue?style=flat-square)
👉 Esta sintaxis puede simplificar cientos de líneas en sistemas de salud, educación o IoT, donde los datos periódicos son la norma.

✅ ¿Por qué?

Porque la repetición de fechas en SQL para insertar series de datos (medicación, sensores, clases, etc.) debería ser natural, no un castigo.
🛠️ Cómo usar

1.  Clona este repositorio
2.  Instala dependencias:

```python
pip install mysql-connector-python
```

3. Ajusta la conexión a tu base de datos en mando_insert_expander.py
4. Ejecuta el script y ¡listo!

## 🧰 Uso por línea de comandos (CLI)

Además del uso básico en Python, este proyecto incluye un script CLI para expandir y ejecutar consultas SQL con rangos de fechas.

Consulta la [Guía CLI](docs/cli-usage.md) para más detalles sobre argumentos, ejecución y configuración de variables de entorno.


📚 ¿Qué sigue?

- [ ] Soporte para saltos: EVERY 2 DAYS
- [x] Sintaxis más flexible
- [x] CLI lista y funcional
- [ ] Web UI (en desarrollo)
- [ ] Integración con VS Code / DataGrip / DBeaver

[![Presentado en HackMeeting v.Φ.I](https://img.shields.io/badge/presentado%20en-hackmeeting%20v.Φ.I-blueviolet)](https://hackmd.io/@t-regexr#H/HΔcKΛΛΣ7ΨΠg-vΦI)

Desarrollado con visión por [@t-regexr](https://github.com/t-regexr)
_A mi madre, visionaria en otra dimensión, que supo reconocer en mí un giro sin tornillo y creyó antes que yo._

---
