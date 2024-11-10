# inventory.py
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Fungsi untuk membuat tampilan halaman inventory
def create_page(parent):
    # Header dengan tema hijau
    header = tk.Label(parent, text="Halaman Inventory", font=("Comic Sans MS", 18, "bold"), bg="#A8D5BA", fg="white", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Frame untuk tombol-tombol utama
    frame_buttons = tk.Frame(parent)
    frame_buttons.pack(pady=20, fill="x")

    # Tombol Build Item
    build_item_button = tk.Button(frame_buttons, text="Build Item", font=("Comic Sans MS", 12), command=build_item)
    build_item_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol Item Register
    item_register_button = tk.Button(frame_buttons, text="Item Register", font=("Comic Sans MS", 12), command=lambda: item_register(parent))
    item_register_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol Inventory Journal
    inventory_journal_button = tk.Button(frame_buttons, text="Inventory Journal", font=("Comic Sans MS", 12), command=inventory_journal)
    inventory_journal_button.pack(side="left", padx=10, fill="x", expand=True)
