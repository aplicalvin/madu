import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Fungsi untuk membuat tampilan halaman 
def create_page(parent):
    # Header dengan tema hijau
    header = tk.Label(parent, text="Sales", font=("Comic Sans MS", 18, "bold"), bg="#A8D5BA", fg="white", anchor="w", padx=20)
    header.pack(fill="x", pady=10)