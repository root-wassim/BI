import pyodbc
import re
import os
from config import SERVER_NAME, DRIVER, SQL_FILE_PATH, DATABASE_NAME

def init_database():
    # Connexion au serveur (base master) pour créer la nouvelle base
    conn_str = f'DRIVER={{{DRIVER}}};SERVER={SERVER_NAME};DATABASE=master;Trusted_Connection=yes;'
    
    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        print(f"✅ Connecté au serveur : {SERVER_NAME}")
    except Exception as e:
        print(f"❌ Échec de connexion. Vérifiez config.py.\nErreur: {e}")
        return

    if not os.path.exists(SQL_FILE_PATH):
        print(f"❌ Fichier SQL introuvable : {SQL_FILE_PATH}")
        return

    print(f"📖 Lecture du script SQL...")
    with open(SQL_FILE_PATH, 'r', encoding='latin-1') as f:
        script = f.read()

    # On sépare par 'GO' car les drivers Python ne comprennent pas cette commande SQL Server
    commands = re.split(r'\bGO\b', script, flags=re.IGNORECASE)
    print(f"🚀 Création de la base '{DATABASE_NAME}'...")

    for cmd in commands:
        stmt = cmd.strip()
        if not stmt: continue
        try:
            cursor.execute(stmt)
        except Exception as e:
            if "Changed database context" not in str(e):
                pass # On ignore les messages d'info
    
    print(f"\n✅ Base de données '{DATABASE_NAME}' prête !")
    conn.close()

if __name__ == "__main__":
    init_database()
