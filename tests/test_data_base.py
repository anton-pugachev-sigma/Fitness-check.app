import pymysql
import pytest
import os
import datetime
from unittest.mock import patch
from src.database import create_connection_fitness_db, insert_workout, select_last_seven_workout
from dotenv import load_dotenv
from src.get_project_root import get_root


@patch("pymysql.connect")
def test_create_connection_mysql_error_returns_none(mock_connect) -> None:
    mock_connect.side_effect = pymysql.MySQLError
    res = create_connection_fitness_db()
    assert res is None


@pytest.fixture
def create_connection():
    roof = get_root()
    dotenv_path = roof / ".env"
    load_dotenv(dotenv_path)
    password_sql = os.getenv("password_my_sql")
    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password=password_sql,
        database="fitness_db",
        cursorclass=pymysql.cursors.DictCursor,  # noqa
    )

    with connection.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS fitness_db_test')
        cursor.execute("USE fitness_db_test")

        query = """
        CREATE TABLE IF NOT EXISTS workout_logs
        LIKE fitness_db.workout_logs;
        """
        cursor.execute(query)

    yield connection

    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE workout_logs')
    connection.close()


def test_insert_workout_success(create_connection) -> None:
    is_insert =  insert_workout(create_connection, '2026-11-21', 'Силовая', 10, 15, 120, 10)

    assert is_insert is True
    with create_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM workout_logs')
        res = cursor.fetchall()


    assert res[0]['day'] == datetime.date(2026, 11, 21)
    assert res[0]['workout_type'] == 'Силовая'



def test_select_last_seven_workout_success(create_connection) -> None:
    _ = insert_workout(create_connection, '2026-11-21', 'Силовая', 10, 15, 120, 10)
    _ = insert_workout(create_connection, '2026-11-21', 'Силовая', 20, 30, 30, 10)
    query = select_last_seven_workout(create_connection)
    res = query[0]

    is_select = query[1]
    assert is_select is True
    assert res[0]['weight'] == 20
    assert res[1]['weight'] == 10

    assert res[0]['repeats'] == 30
    assert res[1]['repeats'] == 15


# def update_workout_by_id(create_connection) -> None:
#     _ = insert_workout(create_connection, '2026-11-21', 'Силовая', 10, 15, 120, 10)
#     _ = insert_workout(create_connection, '2026-11-21', 'Силовая', 20, 30, 30, 10)



    # query = select_last_seven_workout(create_connection)
    # res = query[0]
    #
    # is_select = query[1]
    # assert is_select is True
    # assert res[0]['weight'] == 20
    # assert res[1]['weight'] == 10
    #
    # assert res[0]['repeats'] == 30
    # assert res[1]['repeats'] == 15


