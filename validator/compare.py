# validator/compare.py
import cx_Oracle
import psycopg2
import hashlib

def get_oracle_rows(ora_conn_str, table):
    conn = cx_Oracle.connect(ora_conn_str)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_postgres_rows(pg_conn_str, table):
    conn = psycopg2.connect(pg_conn_str)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    conn.close()
    return rows

def hash_rows(rows):
    row_hashes = set()
    for row in rows:
        joined = '|'.join(str(col) for col in row)
        row_hashes.add(hashlib.md5(joined.encode()).hexdigest())
    return row_hashes

def validate_tables(ora_conn_str, pg_conn_str, table):
    ora_rows = get_oracle_rows(ora_conn_str, table)
    pg_rows = get_postgres_rows(pg_conn_str, table)

    ora_hashes = hash_rows(ora_rows)
    pg_hashes = hash_rows(pg_rows)

    only_in_oracle = ora_hashes - pg_hashes
    only_in_postgres = pg_hashes - ora_hashes

    print(f"\nTable: {table}")
    print(f"Oracle row count: {len(ora_rows)}")
    print(f"PostgreSQL row count: {len(pg_rows)}")
    print(f"Rows only in Oracle: {len(only_in_oracle)}")
    print(f"Rows only in PostgreSQL: {len(only_in_postgres)}")

    if not only_in_oracle and not only_in_postgres:
        print("✅ Tables are in sync!")
    else:
        print("❌ Mismatches detected.")
