import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
from style import apply_styles

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

# Fungsi untuk menampilkan data dalam tabel
def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)
    
    data = get_all_data()
    for row in data:
        tree.insert('', 'end', values=row[1:])  # Menampilkan semua data kecuali ID
    
    # Hitung total debit dan kredit
    total_debit, total_kredit = hitung_total()
    label_total_debit.config(text=f"Total Debit: {total_debit}")
    label_total_kredit.config(text=f"Total Kredit: {total_kredit}")

# Fungsi untuk membuka popup form input data
def popup_input_data():
    def simpan_data():
        tanggal = cal.get_date()
        no_produk = entry_no_produk.get()
        no_akun = entry_no_akun.get()
        nama_akun = entry_nama_akun.get()
        debet = entry_debet.get()
        kredit = entry_kredit.get()
        
        # Validasi input
        if not no_produk or not no_akun or not nama_akun or (not debet and not kredit):
            messagebox.showerror("Error", "Semua kolom harus diisi dengan benar!")
            return
        
        # Atur debet dan kredit secara otomatis
        debet = float(debet) if debet else 0
        kredit = float(kredit) if kredit else 0
        if debet > 0:
            kredit = 0
        if kredit > 0:
            debet = 0
        
        # Simpan data ke database
        tambah_data(tanggal, no_produk, no_akun, nama_akun, debet, kredit)
        tampilkan_data()  # Refresh tabel
        popup.destroy()
    
    # Popup untuk input data
    popup = tk.Toplevel(window)
    popup.title("Tambah Data Akuntansi")
    
    tk.Label(popup, text="Tanggal:").grid(row=0, column=0)
    cal = Calendar(popup, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.grid(row=0, column=1)
    cal.selection_set(datetime.today().date())  # Memilih tanggal default (hari ini)
    
    tk.Label(popup, text="No. Produk:").grid(row=1, column=0)
    entry_no_produk = tk.Entry(popup)
    entry_no_produk.grid(row=1, column=1)
    
    tk.Label(popup, text="No. Akun:").grid(row=2, column=0)
    entry_no_akun = tk.Entry(popup)
    entry_no_akun.grid(row=2, column=1)
    
    tk.Label(popup, text="Nama Akun:").grid(row=3, column=0)
    entry_nama_akun = tk.Entry(popup)
    entry_nama_akun.grid(row=3, column=1)
    
    tk.Label(popup, text="Debet:").grid(row=4, column=0)
    entry_debet = tk.Entry(popup)
    entry_debet.grid(row=4, column=1)
    
    tk.Label(popup, text="Kredit:").grid(row=5, column=0)
    entry_kredit = tk.Entry(popup)
    entry_kredit.grid(row=5, column=1)
    
    # Tombol untuk menyimpan data (gunakan ttk.Button untuk styling)
    ttk.Button(popup, text="Simpan", command=simpan_data, style="TButton").grid(row=6, columnspan=2)


# GUI utama
window = tk.Tk()
window.title("Program Aplikasi Akuntansi")
window.geometry("1200x600")

# Terapkan styling dari file style.py
apply_styles(window)

# Label dan Tombol untuk Menambah Data
tk.Label(window, text="Program Aplikasi Akuntansi", font=("Arial", 18), bg="sky blue").pack(pady=10)

# Ganti tk.Button dengan ttk.Button
ttk.Button(window, text="Tambah Data", command=popup_input_data, style="TButton").pack(pady=10)

# Tabel untuk menampilkan data
columns = ("Tanggal", "No. Produk", "No. Akun", "Nama Akun", "Debet", "Kredit")
tree = ttk.Treeview(window, columns=columns, show="headings", style="Treeview")
for col in columns:
    tree.heading(col, text=col)
tree.pack(pady=10)

# Ganti tk.Label dengan ttk.Label
label_total_debit = ttk.Label(window, text="Total Debit: 0", style="TLabel")
label_total_debit.pack(pady=5)

label_total_kredit = ttk.Label(window, text="Total Kredit: 0", style="TLabel")
label_total_kredit.pack(pady=5)

# Membuat database jika belum ada
create_db()

# Menampilkan data pertama kali
tampilkan_data()

# Menjalankan aplikasi
window.mainloop()
