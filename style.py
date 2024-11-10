# style.py
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

def apply_styles(window):
    # Ganti warna latar belakang window utama menjadi hijau muda
    window.configure(bg='#90EE90')  # Mengubah warna latar belakang utama menjadi hijau muda
    
    # Membuat objek style
    style = ttk.Style()

    # Set style untuk Treeview (tabel)
    style.configure("Treeview",
                    background="#b0e57c",  # Warna latar belakang tabel (hijau muda)
                    foreground="black",
                    fieldbackground="#b0e57c")
    style.configure("Treeview.Heading",
                    background="#90EE90",  # Warna header hijau muda
                    font=("Arial", 10, 'bold'))

    # Set style untuk tombol
    style.configure("TButton",
                    background="#90EE90",  # Warna tombol hijau muda
                    font=("Arial", 10, 'bold'),
                    padding=10)

    # Set style untuk label
    style.configure("TLabel",
                    background="#90EE90",  # Warna latar belakang label hijau muda
                    font=("Arial", 12))
    
    return style
