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

📚 ¿Qué sigue?

```markdown
- Soporte para saltos: EVERY 2 DAYS
- Sintaxis más flexible
- CLI y web UI
- Integración con VS Code / DataGrip / DBeaver
```

Desarrollado con visión por [@t-regexr](https://github.com/t-regexr)
_A mi madre, visionaria en otra dimensión, que supo reconocer en mí un giro sin tornillo y creyó antes que yo._
