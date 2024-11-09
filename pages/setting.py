import tkinter as tk
from tkinter import ttk

def create_page(parent):
    # Frame untuk judul
    header = tk.Label(parent, text="Pengaturan", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)
