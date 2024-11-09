import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sqlite3

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
    # Membersihkan frame konten lama sebelum mengganti dengan konten baru
    for widget in window.winfo_children():
        widget.destroy()
    
    # Frame untuk konten halaman Buku Besar
    frame_content = tk.Frame(window, bg="white")
    frame_content.pack(side="left", fill="both", expand=True)
    
    # Label untuk halaman Buku Besar
    label = tk.Label(frame_content, text="Halaman Buku Besar", font=("Arial", 24), bg="white")
    label.pack(pady=20)
    
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
