import pytest
from validator.compare import hash_rows, validate_tables
from unittest.mock import patch

def test_hash_rows_consistency():
    rows = [(1, 'test', 123), (2, 'abc', 456)]
    result = hash_rows(rows)
    assert len(result) == 2
    assert all(isinstance(h, str) for h in result)

@patch('validator.compare.get_oracle_rows')
@patch('validator.compare.get_postgres_rows')
def test_validate_tables_sync(mock_pg, mock_ora):
    data = [(1, 'a'), (2, 'b')]
    mock_ora.return_value = data
    mock_pg.return_value = data
    validate_tables("fake_oracle", "fake_pg", "test_table")

@patch('validator.compare.get_oracle_rows')
@patch('validator.compare.get_postgres_rows')
def test_validate_tables_mismatch(mock_pg, mock_ora):
    mock_ora.return_value = [(1, 'a'), (2, 'b')]
    mock_pg.return_value = [(1, 'a'), (3, 'c')]
    validate_tables("fake_oracle", "fake_pg", "test_table")
