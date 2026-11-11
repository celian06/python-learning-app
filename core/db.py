import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "progress.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            module_id TEXT PRIMARY KEY,
            completed BOOLEAN,
            quiz_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_progress(module_id, score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO progress (module_id, completed, quiz_score)
        VALUES (?, ?, ?)
    ''', (module_id, True, score))
    
    conn.commit()
    conn.close()