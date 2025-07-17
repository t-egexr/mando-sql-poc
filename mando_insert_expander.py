from datetime import datetime, timedelta
import re
import mysql.connector

# Configura tu conexión
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "mando"
}

def expand_insert(sql):
    pattern = r"VALUES\s*\((\d+),\s*(\d+),\s*FROM\s*'([\d\-]+)'\s*TO\s*'([\d\-]+)'\);"
    match = re.search(pattern, sql)
    if not match:
        raise ValueError("La instrucción no está en el formato esperado.")

    med_id, amount, date_start, date_end = match.groups()
    date_start = datetime.strptime(date_start, "%Y-%m-%d")
    date_end = datetime.strptime(date_end, "%Y-%m-%d")

    values = []
    current_date = date_start
    while current_date <= date_end:
        values.append(f"({med_id}, {amount}, '{current_date.date()}')")
        current_date += timedelta(days=1)

    values_str = ",\n".join(values)
    sql_expanded = re.sub(pattern, f"VALUES\n{values_str};", sql)
    return sql_expanded

# Ejemplo de uso
if __name__ == "__main__":
    original_sql = """
    INSERT INTO dosage (medication_id, amount, date)
    VALUES (5, 3, FROM '2025-04-01' TO '2025-04-05');
    """

    expanded_sql = expand_insert(original_sql)
    print("🔁 SQL Expandido:\n", expanded_sql)

    # Ejecutar en MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS dosage (medication_id INT, amount INT, date DATE);")
    cursor.execute("DELETE FROM dosage;")  # limpiar para pruebas
    cursor.execute(expanded_sql)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Insert ejecutado con éxito.")
