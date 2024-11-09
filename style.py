import tkinter as tk
from tkinter import ttk 
import tkinter as tk
from tkinter import ttk

def apply_styles(window):
    # Styling untuk window utama
    window.configure(bg='sky blue')  # Mengubah warna latar belakang utama
    
    # Membuat objek style
    style = ttk.Style()

    # Set style untuk Treeview (tabel)
    style.configure("Treeview",
                    background="lightblue",
                    foreground="black",
                    fieldbackground="lightblue")
    style.configure("Treeview.Heading",
                    background="skyblue",
                    font=("Arial", 10, 'bold'))

    # Set style untuk tombol
    style.configure("TButton",
                    background="skyblue",
                    font=("Arial", 10, 'bold'),
                    padding=10)

    # Set style untuk label
    style.configure("TLabel",
                    background="skyblue",
                    font=("Arial", 12))
    
    return style
