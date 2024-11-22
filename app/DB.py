import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'status_mhs.sqlite')

def insert_history(jkel, umur, kelas, ips1, ips2, ips3, ips4, ips5, status, model):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Query untuk memasukkan data
    query = """
        INSERT INTO history_pred (jkel, umur, kelas, ips1, ips2, ips3, ips4, ips5, status, model, create_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """
    # Eksekusi query
    cursor.execute(query, (jkel, umur, kelas, ips1, ips2, ips3, ips4, ips5, status, model))
    conn.commit()
    conn.close()

def fetch_history():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Query untuk mengambil semua data dari tabel history_pred
    query = "SELECT * FROM history_pred ORDER BY create_at DESC"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Grafik Jenis Kelamin
    cursor.execute("SELECT jkel, COUNT(*) FROM history_pred GROUP BY jkel")
    gender_data = {row[0]: row[1] for row in cursor.fetchall()}

    # Grafik Kelas
    cursor.execute("SELECT kelas, COUNT(*) FROM history_pred GROUP BY kelas")
    class_data = {row[0]: row[1] for row in cursor.fetchall()}

    # Grafik Status
    cursor.execute("SELECT status, COUNT(*) FROM history_pred GROUP BY status")
    status_data = {row[0]: row[1] for row in cursor.fetchall()}

    # Grafik Model
    cursor.execute("SELECT model, COUNT(*) FROM history_pred GROUP BY model")
    model_data = {row[0]: row[1] for row in cursor.fetchall()}

    # Grafik Per Hari
    cursor.execute("SELECT DATE(create_at), COUNT(*) FROM history_pred GROUP BY DATE(create_at)")
    date_data = {row[0]: row[1] for row in cursor.fetchall()}

    # Tutup koneksi database
    conn.close()

    # Return data dalam format dictionary
    return {
        "history_data": rows,
        "gender_data": gender_data,
        "class_data": class_data,
        "status_data": status_data,
        "model_data": model_data,
        "date_data": date_data
    }

