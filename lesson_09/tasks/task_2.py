import psycopg2
from psycopg2 import sql
from lesson_2.tasks.task_2 import json_dumps as jds
from contextlib import closing
connect_string = "postgres://postgres:postgres@localhost:5432/postgres"


def get_from_table(table_name: str) -> dict:
    """Generator that return sql row
    Args:
        table_name: Name of table. str

    Returns:
        dictionary of sql row {'column_name': value,....}
    """
    with closing(psycopg2.connect(connect_string)) as conn:
        with conn.cursor() as cursor:
            query = sql.SQL("SELECT * FROM public.{};").format(sql.Identifier(table_name))
            try:
                cursor.execute(query)
            except psycopg2.errors.UndefinedTable as ud:
                print(f"{table_name} is Undefined Table")
                return
            column_name = tuple(column.name for column in cursor.description)
            for row in cursor:
                yield dict(zip(column_name, row))


def save_multiline_json(filename: str, table_name: str):
    """Write sql row into file
    Args:
        filename: filename. str
        table_name: table name. str
    """
    rows = get_from_table(table_name)
    with open(f"{filename}.json", 'w') as fp:
        for row in rows:
            fp.write(jds(row))
            fp.write("\n")


if __name__ == "__main__":
    save_multiline_json("out", "github_events")

