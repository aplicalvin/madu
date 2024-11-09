import tkinter as tk
from tkinter import ttk

def create_page(parent):
    # Frame untuk judul
    header = tk.Label(parent, text="Neraca Saldo", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Tabel atau konten untuk halaman Neraca Saldo
    columns = ("No. Akun", "Nama Akun", "Saldo Debit", "Saldo Kredit")
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(pady=10)

    # Label untuk Total Debit dan Kredit
    label_total_debit = tk.Label(parent, text="Total Debit: 0", font=("Arial", 12), bg="sky blue")
    label_total_debit.pack(pady=5)

    label_total_kredit = tk.Label(parent, text="Total Kredit: 0", font=("Arial", 12), bg="sky blue")
    label_total_kredit.pack(pady=5)
