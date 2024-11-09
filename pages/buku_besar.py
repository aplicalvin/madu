import tkinter as tk
from tkinter import ttk
import sqlite3
from navbar import create_sidebar  # Asumsikan fungsi create_sidebar ada di navbar.py

# Fungsi untuk mengambil data Buku Besar dari database
def get_buku_besar_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""
        SELECT tanggal, no_produk, no_akun, nama_akun, debet, kredit
        FROM data_akuntansi
        WHERE debet > 0 OR kredit > 0
        ORDER BY tanggal
    """)
    data = c.fetchall()
    conn.close()
    return data

# Fungsi untuk menampilkan halaman Buku Besar
def load_page(window):
    # Membuat sidebar
    sidebar_width = 200
    sidebar_frame = create_sidebar(window, sidebar_width)

    # Frame untuk konten utama
    frame_content = tk.Frame(window, bg="white")
    frame_content.pack(side="left", fill="both", expand=True)

    # Label untuk judul halaman Buku Besar
    label_header = tk.Label(frame_content, text="Halaman Buku Besar", font=("Arial", 24), bg="white")
    label_header.pack(pady=20)

    # Tabel untuk menampilkan data Buku Besar
    columns = ("Tanggal", "No. Produk", "No. Akun", "Nama Akun", "Debet", "Kredit")
    tree = ttk.Treeview(frame_content, columns=columns, show="headings", style="Treeview")

    # Definisikan heading untuk tabel
    for col in columns:
        tree.heading(col, text=col)

    # Ambil data dari database dan masukkan ke dalam tabel
    data = get_buku_besar_data()
    for row in data:
        tree.insert('', 'end', values=row)

    # Menampilkan tabel di dalam frame
    tree.pack(pady=20, fill="both", expand=True)

    # Menghitung dan menampilkan total debit dan kredit
    total_debit = sum(row[4] for row in data)  # Kolom Debet
    total_kredit = sum(row[5] for row in data)  # Kolom Kredit

    label_total_debit = tk.Label(frame_content, text=f"Total Debit: {total_debit}", font=("Arial", 12), bg="white")
    label_total_debit.pack(pady=5)

    label_total_kredit = tk.Label(frame_content, text=f"Total Kredit: {total_kredit}", font=("Arial", 12), bg="white")
    label_total_kredit.pack(pady=5)

# Main window setup
if __name__ == "__main__":
    # Buat window utama
    window = tk.Tk()
    window.title("Aplikasi Buku Besar")

    # Panggil fungsi untuk load halaman Buku Besar
    load_page(window)

    # Menjalankan aplikasi tkinter
    window.mainloop()
