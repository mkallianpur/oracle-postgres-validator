import argparse
from validator.compare import validate_tables

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate data between Oracle and PostgreSQL tables")
    parser.add_argument("--oracle", required=True, help="Oracle connection string (user/password@host:port/service)")
    parser.add_argument("--postgres", required=True, help="PostgreSQL connection string")
    parser.add_argument("--table", required=True, help="Table name to validate")

    args = parser.parse_args()

    validate_tables(args.oracle, args.postgres, args.table)
