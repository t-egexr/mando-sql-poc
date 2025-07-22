# 🧰 Guía CLI: uso por consola de `mando_insert_expander.py`

Este script también se puede usar desde la terminal para expandir o ejecutar instrucciones SQL que contengan rangos de fechas usando la sintaxis `FROM 'fecha1' TO 'fecha2'`.

---

## ✅ ¿Qué hace el CLI?

1. **Valida la sintaxis y fechas**
   - Detecta errores en el formato `FROM ... TO ...`
   - Avisa si las fechas están mal puestas (por ejemplo, si `TO` es anterior a `FROM`)

2. **Manejo de errores amigable**
   - Si hay fallos de conexión, archivo inexistente o errores SQL, los muestra de forma clara y entendible.

3. **Soporte para argumentos por consola**
   - Puedes ejecutar el script así:

     ```bash
     python mando_insert_expander.py query.sql --execute --user root --password tu_pass --database mando
     ```

4. **Modo seguro: solo expansión**
   - Si solo quieres ver la query expandida, sin ejecutarla:

     ```bash
     python mando_insert_expander.py query.sql
     ```

5. **Uso de variables de entorno**
   - También puedes configurar la conexión con variables, para no pasar la contraseña en la línea:

     ```bash
     export DB_USER=root
     export DB_PASSWORD=tu_pass
     export DB_NAME=mando
     python mando_insert_expander.py query.sql --execute
     ```

---

## 📄 Ejemplo de archivo `query.sql`

```sql
INSERT INTO dosage (medication_id, amount, date)
VALUES (5, 3, FROM '2025-04-01' TO '2025-04-05');
```

🔎 ¿Dónde usarlo?

Este CLI es útil en contextos como:

- Carga masiva de datos diarios en sistemas de salud, educación o IoT
- Automatización desde scripts
- Prototipos rápidos sin escribir loops SQL a mano

---

## 🔐 Seguridad y flexibilidad en la conexión

- Usar **variables de entorno** (`DB_USER`, `DB_PASSWORD`, `DB_NAME`, etc.) permite no exponer credenciales en la línea de comando, ideal para scripts automatizados o entornos compartidos.

- Pasar credenciales vía **argumentos en consola** (`--user`, `--password`, `--database`) da flexibilidad para pruebas rápidas o conexión a múltiples bases sin cambiar el entorno.

Así, el CLI se adapta a distintos usos y niveles de seguridad según tus necesidades.

---

## ⚙️ Cómo crear variables de entorno

### En Linux / macOS (bash/zsh)

```bash
export DB_USER=root
export DB_PASSWORD=tu_pass
export DB_NAME=mando
```
Para que duren en todas las sesiones, agrega estas líneas a tu ~/.bashrc o ~/.zshrc.

### En Windows PowerShell (temporal en la sesión actual)
```powershell
$env:DB_USER = "root"
$env:DB_PASSWORD = "tu_pass"
$env:DB_NAME = "mando"
```
Para hacerlo permanente, usa:
```powershell
setx DB_USER "root"
setx DB_PASSWORD "tu_pass"
setx DB_NAME "mando"
```
Luego cierra y abre la consola.

### En Windows CMD (temporal en la sesión actual)
```cmd
set DB_USER=root
set DB_PASSWORD=tu_pass
set DB_NAME=mando
```
Para hacerlo permanente:
```cmd
setx DB_USER "root"
setx DB_PASSWORD "tu_pass"
setx DB_NAME "mando"
```
luego cierra y abre la consola.

---

Hecho con visión por [@t-regexr](https://github.com/t-regexr)  
Parte de [mando-sql-poc](https://github.com/t-regexr/mando-sql-poc)


