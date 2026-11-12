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

def get_all_progress():
    """Retourne un dictionnaire avec le module_id en clé et le score en valeur."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # On récupère toutes les lignes où le module est marqué comme complété
    cursor.execute("SELECT module_id, quiz_score FROM progress WHERE completed = 1")
    results = cursor.fetchall()
    
    conn.close()
    
    # Transforme la liste de tuples en dictionnaire : {'python_01': 2}
    return {row[0]: row[1] for row in results}