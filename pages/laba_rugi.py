import tkinter as tk
from tkinter import ttk

def create_page(parent):
    # Frame untuk judul
    header = tk.Label(parent, text="Laporan Keuangan Laba Rugi", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Tabel atau konten untuk halaman Laba Rugi
    columns = ("Akun", "Pendapatan", "Beban", "Laba/Rugi")
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(pady=10)

    # Label untuk Total Laba/Rugi
    label_total_laba_rugi = tk.Label(parent, text="Total Laba/Rugi: 0", font=("Arial", 12), bg="sky blue")
    label_total_laba_rugi.pack(pady=5)
