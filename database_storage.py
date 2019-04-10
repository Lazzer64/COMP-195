import sqlite3
import os


# ALL of the global strings could be moved to file and then read instead
streams_table = """
CREATE TABLE streams (
    stream_id integer PRIMARY KEY,
    time_start text NOT NULL,
    time_end text NOT NULL,
    total_bans integer)
"""
stream_insert = """
    INSERT INTO streams (stream_id, time_start, time_end, total_bans)
    VALUES (?, ?, ?, ?)
"""

# Maybe not include 'name' for anonymity
viewers_table = """
CREATE TABLE viewers (
    viewer_id integer PRIMARY KEY,
    name text NOT NULL,
    streams_joined integer NOT NULL)
"""
viewer_insert = """
    INSERT INTO viewers (viewer_id, name, streams_joined)
    VALUES (?, ?, ?)
"""

# Could just store the csv file location instead and remove this table
stream_chat_table = """
CREATE TABLE stream_chat (
    stream_id integer NOT NULL,
    viewer_id integer NOT NULL,
    message text NOT NULL,
    timestamp text NOT NULL,
    verdict text NOT NULL,
    FOREIGN KEY (stream_id) REFERENCES streams (stream_id),
    FOREIGN KEY (viewer_id) REFERENCES viewers (viewer_id))
"""
chat_insert = """
    INSERT INTO stream_chat (stream_id, viewer_id, message, timestamp, verdict)
    VALUES (?, ?, ?, ?, ?)
"""

debug_delete_db = True  # Only set True if you want the current database deleted

tables = [streams_table, viewers_table, stream_chat_table]
inserts = {'streams': stream_insert, 'viewers': viewer_insert, 'stream_chat': chat_insert}
db = None
db_path = 'database.sqlite3'


def database_store(table, data):
    cur = db.cursor()

    if table in inserts:
        cur.executemany(inserts[table], data)
    else:
        # TODO log error?
        pass


def query_data(table):
    sql = "SELECT * FROM " + table
    cur = db.cursor()
    cur.execute(sql)
    return cur.fetchall()


def create_db():
    global db
    if os.path.isfile(db_path) and debug_delete_db:
        os.remove(db_path)

    if not os.path.isfile(db_path):
        db = sqlite3.connect(db_path)
        cur = db.cursor()
        for table in tables:
            cur.execute(table)


if __name__ == '__main__':
    create_db()

    database_store('streams', [(1, '5pm', '6pm', 0), (2, '5am', '6am', 0)])

    print(query_data('streams'))
