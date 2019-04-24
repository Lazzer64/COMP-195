import sqlite3

from datetime import datetime

from flask import g

from database_storage import db_path

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db

def moderation_enabled(channel_id, *, enabled=None):
    db = get_db()

    if enabled is None:
        response = db.execute("SELECT enabled FROM moderation WHERE channel_id = ?", (channel_id,))
        row = response.fetchone()
        if row is not None:
            return bool(row[0])
        return False

    db.execute("INSERT OR REPLACE INTO moderation (channel_id, enabled) VALUES (?, ?)", (channel_id, enabled))
    db.commit()
    return enabled

def logs(channel_id, *, time=None, message=None):
    db = get_db()

    if message:
        timestamp = time if time is not None else datetime.now()
        db.execute("INSERT INTO log_message (channel_id, timestamp, message) VALUES (?, ?, ?)",
                   (channel_id, timestamp, message))
        db.commit()

    response = db.execute("SELECT timestamp, message FROM log_message WHERE channel_id = ? ORDER BY timestamp DESC", (channel_id,))
    return response.fetchall()

def emotes(channel_id):
    db = get_db()
    response = db.execute("SELECT emote, count FROM emotes WHERE channel_id = ?", (channel_id,))

    emotes = {}
    for emote, count in response.fetchall():
        emotes[emote] = count

    return emotes

def viewers(channel_id):
    return {"Sunday (1/1)": 1237,
            "Monday (1/2)": 5238,
            "Tuesday (1/2)": 2927,
            "Wednesday (1/3)": 8389,
            "Thursday (1/4)": 1783,
            "Friday (1/5)": 8427,
            "Saturday (1/6)": 4483}
