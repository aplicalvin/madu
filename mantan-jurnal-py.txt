# jurnal.py
import sqlite3
from datetime import datetime

# Fungsi untuk membuat koneksi dan tabel di database SQLite
def create_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data_akuntansi (
                    id INTEGER PRIMARY KEY,
                    tanggal TEXT,
                    no_produk TEXT,
                    no_akun TEXT,
                    nama_akun TEXT,
                    debet REAL,
                    kredit REAL)''')
    conn.commit()
    conn.close()

# Fungsi untuk menambah data ke database
def tambah_data(tanggal, no_produk, no_akun, nama_akun, debet, kredit):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO data_akuntansi (tanggal, no_produk, no_akun, nama_akun, debet, kredit) VALUES (?, ?, ?, ?, ?, ?)",
              (tanggal, no_produk, no_akun, nama_akun, debet, kredit))
    conn.commit()
    conn.close()

# Fungsi untuk mengambil semua data dari database
def get_all_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data_akuntansi")
    data = c.fetchall()
    conn.close()
    return data

# Fungsi untuk menghitung total debit dan kredit
def hitung_total():
    data = get_all_data()
    total_debit = sum(row[5] for row in data)  # Kolom debet
    total_kredit = sum(row[6] for row in data)  # Kolom kredit
    return total_debit, total_kredit
