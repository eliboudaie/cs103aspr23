import pytest
import os
import tempfile
from transaction import Transaction


@pytest.fixture
def db():
  db_fd, db_name = tempfile.mkstemp()
  yield db_name
  os.close(db_fd)
  os.unlink(db_name)


def test_create_table(db):
  t = Transaction(db)
  t.create_table()
  conn = t.conn
  cursor = t.cursor
  cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';"
  )
  assert cursor.fetchone()[0] == 'transactions'
  cursor.close()
  conn.close()


def test_add_transaction(db):
  t = Transaction(db)
  t.create_table()
  t.add_transaction(1, 10.0, 'Food', '2022-03-15', 'Lunch')
  conn = t.conn
  cursor = t.cursor
  cursor.execute("SELECT * FROM transactions;")
  rows = cursor.fetchall()
  assert len(rows) == 1
  assert rows[0][1] == 1
  assert rows[0][2] == 10.0
  assert rows[0][3] == 'Food'
  assert rows[0][4] == '2022-03-15'
  assert rows[0][5] == 'Lunch'
  cursor.close()
  conn.close()


def test_get_transactions(db):
  t = Transaction(db)
  t.create_table()
  t.add_transaction(1, 10.0, 'Food', '2022-03-15', 'Lunch')
  t.add_transaction(2, 20.0, 'Transportation', '2022-03-15', 'Taxi')
  conn = t.conn
  cursor = t.cursor
  rows = t.get_transactions()
  assert len(rows) == 2
  assert rows[0][1] == 1
  assert rows[0][2] == 10.0
  assert rows[0][3] == 'Food'
  assert rows[0][4] == '2022-03-15'
  assert rows[0][5] == 'Lunch'
  assert rows[1][1] == 2
  assert rows[1][2] == 20.0
  assert rows[1][3] == 'Transportation'
  assert rows[1][4] == '2022-03-15'
  assert rows[1][5] == 'Taxi'
  cursor.close()
  conn.close()


def test_get_transaction_by_id(db):
  t = Transaction(db)
  t.create_table()
  t.add_transaction(1, 10.0, 'Food', '2022-03-15', 'Lunch')
  t.add_transaction(2, 20.0, 'Transportation', '2022-03-15', 'Taxi')
  conn = t.conn
  cursor = t.cursor
  row = t.get_transaction_by_id(1)
  assert row[1] == 1
  assert row[2] == 10.0
  assert row[3] == 'Food'
  assert row[4] == '2022-03-15'
  assert row[5] == 'Lunch'
  cursor.close()
  conn.close()

def test_get_categories(db):
  t = Transaction(db)
  t.create_table()
  t.add_transaction(1, 10.0, 'Food', '2022-03-15', 'Lunch')
  t.add_transaction(2, 20.0, 'Transportation', '2022-03-15', 'Taxi')
  conn = t.conn
  cursor = t.cursor
  rows = t.get_categories()()
  assert row[1] == 'Food'
  assert row[2] == 'Transportation'
  cursor.close()
  conn.close()