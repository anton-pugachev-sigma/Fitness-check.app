import os
import pymysql.cursors
from dotenv import load_dotenv
from src.get_project_root import get_root

roof = get_root()
dotenv_path = roof / ".env"
load_dotenv(dotenv_path)
password_sql = os.getenv("password_my_sql")


def create_connection_fitness_db():
    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password=password_sql,
            database="fitness_db",
            cursorclass=pymysql.cursors.DictCursor,  # noqa
        )
        return connection

    except pymysql.MySQLError:
        return None


def insert_workout(
    connection: pymysql.Connection,
    day: str,
    workout_type: str,
    weight: int,
    repeats: int,
    rest_time: int,
    score: int,
):
    data_workout = {
        "day": day,
        "workout_type": workout_type,
        "weight": weight,
        "repeats": repeats,
        "rest_time": rest_time,
        "score": score,
    }
    connection.ping()

    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO workout_logs
            (day, workout_type, weight, repeats, rest_time, score)
            VALUES (%(day)s, %(workout_type)s, %(weight)s, %(repeats)s, %(rest_time)s, %(score)s)
            """
            cursor.execute(query, data_workout)
            connection.commit()
            return True

    except pymysql.MySQLError:
        return False


def select_last_seven_workout(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id, workout_type, weight, repeats, rest_time
                 FROM workout_logs
                 ORDER BY id DESC
                 LIMIT 7;
                 """)
            rows = cursor.fetchall()
            return rows[::-1]
    except Exception as e:
        print(f"Что-то пошло не так, код ошибки:{e}")


# def update_workout_by_id(connection):
#     try:
#         with connection.cursor() as cursor:
#             query = """
#             UPDATE workout_logs
#             SET repeats = 15
#             WHERE id=2"""
#             update_query = cursor.execute(query)
#             connection.commit()
#     except Exception as e:
#         print(f"Что-то пошло не так, код ошибки:{e}")
#
#         """
#         if insert_workout:
#         insert_workout(connection)
#         """
#
#         """
#         if select_last_seven_workout:
#             select_last_seven_workout(connection)
#         """
#
#         """
#         if update_workout_by_id:
#            update_workout_by_id(connection)
#         """
