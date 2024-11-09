import tkinter as tk
from tkinter import ttk

def create_page(parent):
    # Frame untuk judul
    header = tk.Label(parent, text="Laporan Keuangan Ekuitas", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Tabel atau konten untuk halaman Ekuitas
    columns = ("No. Akun", "Nama Akun", "Saldo Awal", "Saldo Akhir")
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(pady=10)

    # Label untuk Total Ekuitas
    label_total_ekuitas = tk.Label(parent, text="Total Ekuitas: 0", font=("Arial", 12), bg="sky blue")
    label_total_ekuitas.pack(pady=5)
