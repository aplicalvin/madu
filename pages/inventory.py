import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Membuka koneksi ke database
def connect_db():
    return sqlite3.connect('inventory.db')

# Membuat tabel jika belum ada
def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kode_item_teh TEXT NOT NULL,
                    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
                    memo TEXT)''')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan item
def build_item():
    def save_item():
        kode_item_teh = kode_item_entry.get()
        memo = memo_entry.get()
        date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = connect_db()
        c = conn.cursor()
        c.execute('''INSERT INTO inventory (kode_item_teh, date_added, memo) 
                     VALUES (?, ?, ?)''', (kode_item_teh, date_added, memo))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Item successfully added.")
        build_item_window.destroy()

    build_item_window = tk.Toplevel()
    build_item_window.title("Build Item")
    
    tk.Label(build_item_window, text="Kode Item Teh").pack(pady=5)
    kode_item_entry = tk.Entry(build_item_window)
    kode_item_entry.pack(pady=5)
    
    tk.Label(build_item_window, text="Memo").pack(pady=5)
    memo_entry = tk.Entry(build_item_window)
    memo_entry.pack(pady=5)

    tk.Button(build_item_window, text="Save Item", command=save_item).pack(pady=20)

# Fungsi untuk menampilkan daftar item dengan filter tanggal
def item_register(parent):
    def filter_items():
        filter_date = date_filter_entry.get()
        conn = connect_db()
        c = conn.cursor()
        if filter_date:
            c.execute("SELECT * FROM inventory WHERE date_added LIKE ?", (filter_date+'%',))
        else:
            c.execute("SELECT * FROM inventory")
        rows = c.fetchall()
        conn.close()
        
        # Update Treeview
        for row in tree.get_children():
            tree.delete(row)
        
        for row in rows:
            tree.insert("", "end", values=row)

    item_register_window = tk.Toplevel(parent)
    item_register_window.title("Item Register")

    # Filter by Date
    tk.Label(item_register_window, text="Filter by Date (YYYY-MM-DD):").pack(pady=5)
    date_filter_entry = tk.Entry(item_register_window)
    date_filter_entry.pack(pady=5)
    
    tk.Button(item_register_window, text="Filter", command=filter_items).pack(pady=10)

    # Treeview untuk menampilkan data
    columns = ("item_id", "kode_item_teh", "date_added", "memo")
    tree = ttk.Treeview(item_register_window, columns=columns, show="headings")
    tree.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)

    # Memanggil data awal
    filter_items()

# Fungsi untuk halaman jurnal inventaris
def inventory_journal():
    def load_journal():
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM inventory ORDER BY date_added DESC")
        rows = c.fetchall()
        conn.close()

        # Clear the existing treeview
        for row in tree.get_children():
            tree.delete(row)

        # Insert the new data
        for row in rows:
            tree.insert("", "end", values=row)

    def add_journal_entry():
        kode_item_teh = kode_item_entry.get()
        memo = memo_entry.get()
        if not kode_item_teh or not memo:
            messagebox.showwarning("Input Error", "Please fill in both fields!")
            return
        
        date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = connect_db()
        c = conn.cursor()
        c.execute('''INSERT INTO inventory (kode_item_teh, date_added, memo) 
                     VALUES (?, ?, ?)''', (kode_item_teh, date_added, memo))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Journal entry added successfully.")
        load_journal()
    
    inventory_journal_window = tk.Toplevel()
    inventory_journal_window.title("Inventory Journal")

    # Input fields for new journal entry
    tk.Label(inventory_journal_window, text="Kode Item Teh:").pack(pady=5)
    kode_item_entry = tk.Entry(inventory_journal_window)
    kode_item_entry.pack(pady=5)

    tk.Label(inventory_journal_window, text="Memo:").pack(pady=5)
    memo_entry = tk.Entry(inventory_journal_window)
    memo_entry.pack(pady=5)

    tk.Button(inventory_journal_window, text="Add Journal Entry", command=add_journal_entry).pack(pady=10)

    # Treeview to display journal entries
    columns = ("item_id", "kode_item_teh", "date_added", "memo")
    tree = ttk.Treeview(inventory_journal_window, columns=columns, show="headings")
    tree.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)

    # Load the journal entries
    load_journal()

# Halaman utama dengan tombol
def create_page(parent):
    create_table()  # Membuat tabel jika belum ada
    
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
