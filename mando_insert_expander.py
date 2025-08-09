# mando_insert_expander.py
# Licencia MIT (c) 2025 t-regexrr
# https://github.com/t-regexr/mando-sql-poc

import re
import sys
import argparse
import os
from datetime import datetime, timedelta
import mysql.connector

def detect_type(value):
    """Detecta el tipo SQL basado en el valor del string."""
    val = value.strip()
    if val.lower() in ("true", "false"):
        return "BOOLEAN"
    if val.startswith("'") and val.endswith("'"):
        return "VARCHAR(255)"
    try:
        int(val)
        return "INT"
    except ValueError:
        pass
    try:
        float(val)
        return "FLOAT"
    except ValueError:
        pass
    # Por defecto VARCHAR
    return "VARCHAR(255)"

def create_table_dynamic(cursor, table_name, columns, values):
    # Detectar tipos para cada columna excepto la última (fecha)
    cols_sql = []
    for col, val in zip(columns[:-1], values):
        col_type = detect_type(val)
        cols_sql.append(f"{col} {col_type}")
    # La última columna es fecha
    cols_sql.append(f"{columns[-1]} DATE")

    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols_sql)});"
    print(f"Creando tabla si no existe:\n{create_sql}")
    cursor.execute(create_sql)

def parse_value(val):
    """Convierte el valor de string a su forma para insertar en SQL."""
    val = val.strip()
    if val.lower() in ("true", "false"):
        return val.upper()
    return val

def expand_insert(sql):
    # Regex para capturar tabla, columnas, valores fijos y fechas
    pattern = re.compile(
        r"INSERT\s+INTO\s+(\w+)\s*"  # tabla
        r"\(([\w\s,]+)\)\s*"          # columnas
        r"VALUES\s*\(\s*([^\)]+)\s*\)\s*,\s*"  # valores fijos (cualquier cosa excepto ')')
        r"FROM\s*'(\d{4}-\d{2}-\d{2})'\s*TO\s*'(\d{4}-\d{2}-\d{2})'",
        re.IGNORECASE
    )

    match = pattern.search(sql)
    if not match:
        raise ValueError("Formato SQL incorrecto. Debe ser: INSERT INTO tabla (cols) VALUES (valores), FROM 'YYYY-MM-DD' TO 'YYYY-MM-DD'")

    table_name = match.group(1)
    columns_str = match.group(2)
    values_str = match.group(3)
    date_start_str = match.group(4)
    date_end_str = match.group(5)

    columns = [col.strip() for col in columns_str.split(",")]
    # Separar valores fijos respetando comillas
    values = []
    temp = ""
    in_quotes = False
    for c in values_str:
        if c == "'" and not in_quotes:
            in_quotes = True
            temp += c
        elif c == "'" and in_quotes:
            in_quotes = False
            temp += c
        elif c == "," and not in_quotes:
            values.append(temp.strip())
            temp = ""
        else:
            temp += c
    if temp:
        values.append(temp.strip())

    if len(columns) != len(values) + 1:
        # +1 porque la última columna debe ser 'date' sin valor fijo
        raise ValueError(f"Número de columnas ({len(columns)}) debe ser igual a número de valores ({len(values)}) + 1 (la columna de fecha)")

    if columns[-1].lower() != 'date':
        raise ValueError("La última columna debe ser 'date' para el rango dinámico")

    # Validar fechas
    try:
        date_start = datetime.strptime(date_start_str, "%Y-%m-%d")
        date_end = datetime.strptime(date_end_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Formato de fecha inválido. Debe ser YYYY-MM-DD")

    if date_end < date_start:
        raise ValueError("La fecha 'TO' no puede ser anterior a 'FROM'")

    # Construir valores para cada fecha en rango
    values_list = []
    current_date = date_start
    while current_date <= date_end:
        date_val = f"'{current_date.strftime('%Y-%m-%d')}'"
        vals_parsed = [parse_value(v) for v in values] + [date_val]
        vals_sql = ", ".join(str(v) for v in vals_parsed)
        values_list.append(f"({vals_sql})")
        current_date += timedelta(days=1)

    values_sql = ",\n".join(values_list)
    columns_sql = ", ".join(columns)
    expanded_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES\n{values_sql};"

    return table_name, columns, values, expanded_sql

def execute_sql(sql, db_config, table_name, columns, values):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Crear tabla dinámicamente con tipos detectados
        create_table_dynamic(cursor, table_name, columns, values)

        print("Limpiando tabla para pruebas...")
        cursor.execute(f"DELETE FROM {table_name};")

        print("Ejecutando SQL expandido...")
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()
        print("Inserción exitosa.")
    except mysql.connector.Error as err:
        print(f"Error en MySQL: {err}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Expande e inserta SQL con rango de fechas y tipos detectados")
    parser.add_argument("sqlfile", help="Archivo con la instrucción SQL a expandir")
    parser.add_argument("--execute", action="store_true", help="Ejecutar la query expandida en la base de datos")
    parser.add_argument("--host", default=os.getenv("DB_HOST", "localhost"), help="Host de la base de datos")
    parser.add_argument("--user", default=os.getenv("DB_USER", "root"), help="Usuario de la base de datos")
    parser.add_argument("--password", default=os.getenv("DB_PASSWORD", ""), help="Contraseña de la base de datos")
    parser.add_argument("--database", default=os.getenv("DB_NAME", "mando"), help="Nombre de la base de datos")

    args = parser.parse_args()

    try:
        with open(args.sqlfile, "r", encoding="utf-8") as f:
            original_sql = f.read()
    except FileNotFoundError:
        print(f"Archivo no encontrado: {args.sqlfile}")
        sys.exit(1)

    try:
        table_name, columns, values, expanded_sql = expand_insert(original_sql)
    except ValueError as e:
        print(f"Error al expandir la consulta: {e}")
        sys.exit(1)

    print("SQL expandido:\n", expanded_sql)

    if args.execute:
        db_config = {
            "host": args.host,
            "user": args.user,
            "password": args.password,
            "database": args.database,
        }
        execute_sql(expanded_sql, db_config, table_name, columns, values)
    else:
        print("La consulta no se ejecutó. Usa --execute para ejecutar en la base de datos.")

if __name__ == "__main__":
    main()
