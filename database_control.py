import sqlite3

# Fungsi untuk membuat koneksi dan tabel di database SQLite
def create_db():
    conn = sqlite3.connect('data.db')  # Koneksi ke database
    c = conn.cursor()  # Membuat cursor untuk eksekusi query

    # Membuat tabel users (untuk login pengguna)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    nama TEXT NOT NULL)''')


    # Membuat tabel inventory (untuk menyimpan data barang dalam inventaris)
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    date_added DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Membuat tabel accounts (untuk akun-akun yang digunakan dalam jurnal akuntansi)
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_name TEXT NOT NULL,
                    balance REAL NOT NULL DEFAULT 0)''')

    # Membuat tabel journal_entries (untuk mencatat transaksi jurnal akuntansi)
    c.execute('''CREATE TABLE IF NOT EXISTS journal_entries (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER,
                    amount REAL NOT NULL,
                    entry_type TEXT NOT NULL, -- debit atau credit
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id))''')

    # Membuat tabel transactions (untuk mencatat transaksi umum, misalnya penjualan atau pembelian)
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL, -- sales, purchase, cash receipt, dll.
                    amount REAL NOT NULL,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Membuat tabel sales_and_purchases (untuk transaksi penjualan atau pembelian barang)
    c.execute('''CREATE TABLE IF NOT EXISTS sales_and_purchases (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER,
                    quantity INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    payment_type TEXT, -- cash, qris, dll.
                    FOREIGN KEY (item_id) REFERENCES inventory(item_id),
                    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id))''')

    # Commit perubahan dan menutup koneksi
    conn.commit()
    conn.close()

# Panggil fungsi untuk membuat tabel di database
create_db()