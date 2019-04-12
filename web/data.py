import sqlite3

from flask import g

from database_storage import db_path

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db

def moderation_enabled(channel_id, enabled=None):
    db = get_db()
    if enabled is None:
        response = db.execute("SELECT enabled FROM moderation WHERE channel_id = ?", (channel_id,))
        row = response.fetchone()
        if row is not None:
            return bool(row[0])
        return False

    db.execute("UPDATE moderation SET enabled = ? WHERE channel_id = ?", (enabled, channel_id))
    db.commit()
    return enabled

def logs(channel_id):
    db = get_db()
    response = db.execute("SELECT timestamp, message FROM log_message WHERE channel_id = ? ORDER BY timestamp DESC", (channel_id,))
    return response.fetchall()

def emotes(channel_id):
    db = get_db()
    response = db.execute("SELECT emote, count FROM emotes WHERE channel_id = ?", (channel_id,))

    emotes = {}
    for emote, count in response.fetchall():
        emotes[emote] = count

    return emotes
