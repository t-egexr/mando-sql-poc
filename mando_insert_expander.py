# mando_insert_expander.py
# MIT License (c) 2025 @t-regexr
# https://github.com/t-regexr/mando-sql-poc

import re
import argparse
from datetime import datetime, timedelta
import mysql.connector
import sys
import os

def expand_insert(sql):
    # Regex más flexible (case insensitive, espacios variables)
    pattern = re.compile(
        r"VALUES\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*FROM\s*'([\d\-]+)'\s*TO\s*'([\d\-]+)'\s*\)\s*;",
        re.IGNORECASE
    )
    match = pattern.search(sql)
    if not match:
        raise ValueError("La instrucción no está en el formato esperado: VALUES (..., FROM 'YYYY-MM-DD' TO 'YYYY-MM-DD');")

    med_id, amount, date_start_str, date_end_str = match.groups()

    # Validar fechas
    try:
        date_start = datetime.strptime(date_start_str, "%Y-%m-%d")
        date_end = datetime.strptime(date_end_str, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Formato de fecha inválido: {e}")

    if date_end < date_start:
        raise ValueError("La fecha 'TO' no puede ser anterior a la fecha 'FROM'.")

    values = []
    current_date = date_start
    while current_date <= date_end:
        values.append(f"({med_id}, {amount}, '{current_date.date()}')")
        current_date += timedelta(days=1)

    values_str = ",\n".join(values)
    sql_expanded = pattern.sub(f"VALUES\n{values_str};", sql)
    return sql_expanded

def execute_sql(sql, db_config):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("🔧 Creando tabla si no existe...")
        cursor.execute("CREATE TABLE IF NOT EXISTS dosage (medication_id INT, amount INT, date DATE);")
        print("🧹 Limpiando tabla para pruebas...")
        cursor.execute("DELETE FROM dosage;")
        print("🚀 Ejecutando SQL expandido...")
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Insert ejecutado con éxito.")
    except mysql.connector.Error as err:
        print(f"❌ Error en MySQL: {err}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Expande y ejecuta SQL con sintaxis especial INSERT ... FROM ... TO ...")
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
        print(f"❌ Archivo no encontrado: {args.sqlfile}")
        sys.exit(1)

    try:
        expanded_sql = expand_insert(original_sql)
    except ValueError as e:
        print(f"❌ Error al expandir la consulta: {e}")
        sys.exit(1)

    print("🔁 SQL Expandido:\n", expanded_sql)

    if args.execute:
        db_config = {
            "host": args.host,
            "user": args.user,
            "password": args.password,
            "database": args.database,
        }
        execute_sql(expanded_sql, db_config)
    else:
        print("\n⚠️ La query no se ejecutó. Usa --execute para ejecutar en la base de datos.")

if __name__ == "__main__":
    main()
