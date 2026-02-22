import sqlite3

# Nome del file databaset SQlite utilizzato
NOME_DB = "gestione_spese.db"

# Crea il database e la tabella 'spese' se non esistono, chiamata all'avvio dell'applicazione
def inizializza_db():
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS spese (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_articolo TEXT,
        importo REAL,
        data TEXT,
        categoria TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Inserisce una nuova spesa nel database
def salva_spesa_db(nome_art, importo_art, data_art, categoria_art):
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO spese (nome_articolo, importo, data, categoria)
        VALUES (?, ?, ?, ?)
        ''', (nome_art, importo_art, data_art, categoria_art))
    conn.commit()
    conn.close()

# Restituisce tutte le spese salvate nel database
def visualizza_spese_db():
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spese")
    dati = cursor.fetchall()
    conn.close()
    return dati

# Elimina una spesa tramite il relativo ID
def elimina_spesa_db(id):
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spese WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Calcola il totale delle spese salvate e ritorna l'importo (somma totale)
def visualizza_importo_db():
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(importo) FROM spese")
    dati = cursor.fetchall()[0][0]
    conn.close()
    return dati

# Restituisce le spese per mese-anno
def visualizza_grafico_spese_db():
    conn = sqlite3.connect("gestione_spese.db")
    cursor = conn.cursor()

    cursor.execute("""
            SELECT substr(data, 4, 7) AS mese_anno, SUM(importo) 
            FROM spese 
            GROUP BY mese_anno 
            ORDER BY substr(data, 7, 4), substr(data, 4, 2)
        """)

    dati = cursor.fetchall()
    conn.close()
    return dati