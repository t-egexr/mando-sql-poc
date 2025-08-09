✅ Versión actualizada de docs/cli-usage.md

# 🧰 Guía CLI: uso por consola de `mando_insert_expander.py`

Este script también se puede usar desde la terminal para expandir o ejecutar instrucciones SQL que contengan rangos de fechas con la sintaxis especial:

```sql
VALUES (..., FROM 'YYYY-MM-DD' TO 'YYYY-MM-DD');
```

✅ ¿Qué hace el CLI?

+ Expande automáticamente las fechas
+ Convierte rangos FROM ... TO ... en múltiples filas individuales.
+ Crea la tabla si no existe
+ Detecta nombres y columnas desde la query.
+ Deduce tipos (INT, VARCHAR, etc.) automáticamente.
+ Valida sintaxis y fechas
+ Avisa si TO es anterior a FROM.
+ Muestra errores si el formato es incorrecto.
+ Manejo de errores amigable
+ Reportes claros en caso de error SQL, conexión fallida o archivo faltante.
+ Soporte completo por argumentos

Ejemplo de uso básico:

```bash
python mando_insert_expander.py query.sql --execute --user root --password tu_pass --database mando
```

Modo seguro (solo expansión, sin ejecución)

```bash
python mando_insert_expander.py query.sql
```

Variables de entorno
    
Puedes evitar poner la contraseña en la línea de comandos:

```bash
export DB_USER=root
export DB_PASSWORD=tu_pass
export DB_NAME=mando
python mando_insert_expander.py query.sql --execute
```

---

📄 Ejemplo de archivo query.sql

```sql
INSERT INTO dosage (medication_id, amount, date)
VALUES (5, 3, FROM '2025-04-01' TO '2025-04-05');
```

---

🆕 También soporta múltiples columnas y tipos de datos. Por ejemplo:

```sql
INSERT INTO dosage (medication_id, amount, id_user, is_active, date)
VALUES (5, 3, 10, true, FROM '2025-01-01' TO '2025-01-03');
```

---

🔎 ¿Dónde usarlo?

Ideal en contextos como:

+ Carga masiva de datos diarios en salud, educación o IoT
+ Automatización de pruebas de estrés
+ Scripts de integración o mantenimiento
+ Prototipos sin necesidad de ORMs o herramientas pesadas

---

🔐 Seguridad y flexibilidad en la conexión

Variables de entorno (DB_USER, DB_PASSWORD, DB_NAME)
+ Buenas para entornos seguros y scripts automatizados.

Argumentos por línea de comandos
+ Útiles para pruebas rápidas o conexiones puntuales.

---

⚙️ Cómo crear variables de entorno

En Linux / macOS (bash/zsh)

```bash
export DB_USER=root
export DB_PASSWORD=tu_pass
export DB_NAME=mando
```

Para que sean permanentes, agrega esas líneas a ~/.bashrc o ~/.zshrc.

En Windows PowerShell (temporal)

```powershell
$env:DB_USER = "root"
$env:DB_PASSWORD = "tu_pass"
$env:DB_NAME = "mando"
```

Permanente:

```powershell
setx DB_USER "root"
setx DB_PASSWORD "tu_pass"
setx DB_NAME "mando"
```
En Windows CMD (temporal)

```cmd
set DB_USER=root
set DB_PASSWORD=tu_pass
set DB_NAME=mando
```

Permanente:

```cmd
setx DB_USER "root"
setx DB_PASSWORD "tu_pass"
setx DB_NAME "mando"
```

---

Hecho con visión por @t-regexr
Parte de mando-sql-poc
