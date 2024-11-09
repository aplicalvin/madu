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
                    kredit REAL,
                    upd_saldo REAL)''')
    conn.commit()
    conn.close()


