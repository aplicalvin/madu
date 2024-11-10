import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Membuka koneksi ke database
def connect_db():
    return sqlite3.connect('accounting.db')

# Membuat tabel jika belum ada
def create_table():
    conn = connect_db()
    c = conn.cursor()

    # Tabel untuk menyimpan akun-akun
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number TEXT NOT NULL,
                    account_name TEXT NOT NULL,
                    account_type TEXT NOT NULL)''')

    # Tabel untuk menyimpan jurnal
    c.execute('''CREATE TABLE IF NOT EXISTS journal_entries (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    debit REAL,
                    credit REAL,
                    memo TEXT,
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id))''')

    # Tabel untuk menyimpan transaksi
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    account_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id))''')

    conn.commit()
    conn.close()

# Fungsi untuk menampilkan dan mengedit daftar akun
def account_list():
    def display_accounts():
        # Mengambil data akun dari database
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM accounts")
        rows = c.fetchall()
        conn.close()

        # Menghapus data yang ada di Treeview sebelum memasukkan data terbaru
        for row in tree.get_children():
            tree.delete(row)

        # Menambahkan data akun ke Treeview
        for row in rows:
            tree.insert("", "end", values=row)

    def add_account():
        def save_account():
            account_number = acc_number_entry.get()
            account_name = acc_name_entry.get()
            account_type = acc_type_entry.get()

            # Menyimpan data akun ke database
            conn = connect_db()
            c = conn.cursor()
            c.execute('''INSERT INTO accounts (account_number, account_name, account_type) 
                         VALUES (?, ?, ?)''', (account_number, account_name, account_type))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account successfully added.")
            add_account_window.destroy()
            display_accounts()

        # Popup untuk menambahkan akun
        add_account_window = tk.Toplevel()
        add_account_window.title("Add Account")

        tk.Label(add_account_window, text="Account Number").pack(pady=5)
        acc_number_entry = tk.Entry(add_account_window)
        acc_number_entry.pack(pady=5)

        tk.Label(add_account_window, text="Account Name").pack(pady=5)
        acc_name_entry = tk.Entry(add_account_window)
        acc_name_entry.pack(pady=5)

        tk.Label(add_account_window, text="Account Type").pack(pady=5)
        acc_type_entry = tk.Entry(add_account_window)
        acc_type_entry.pack(pady=5)

        tk.Button(add_account_window, text="Save Account", command=save_account).pack(pady=20)

    def edit_account(account_id):
        def update_account():
            account_number = acc_number_entry.get()
            account_name = acc_name_entry.get()
            account_type = acc_type_entry.get()

            # Update akun yang dipilih
            conn = connect_db()
            c = conn.cursor()
            c.execute('''UPDATE accounts SET account_number = ?, account_name = ?, account_type = ?
                         WHERE account_id = ?''', (account_number, account_name, account_type, account_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account successfully updated.")
            edit_account_window.destroy()
            display_accounts()

        # Popup untuk mengedit akun
        edit_account_window = tk.Toplevel()
        edit_account_window.title("Edit Account")

        # Mengambil data akun yang akan diedit
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
        account = c.fetchone()
        conn.close()

        # Form untuk mengedit data akun
        tk.Label(edit_account_window, text="Account Number").pack(pady=5)
        acc_number_entry = tk.Entry(edit_account_window)
        acc_number_entry.insert(0, account[1])  # account_number
        acc_number_entry.pack(pady=5)

        tk.Label(edit_account_window, text="Account Name").pack(pady=5)
        acc_name_entry = tk.Entry(edit_account_window)
        acc_name_entry.insert(0, account[2])  # account_name
        acc_name_entry.pack(pady=5)

        tk.Label(edit_account_window, text="Account Type").pack(pady=5)
        acc_type_entry = tk.Entry(edit_account_window)
        acc_type_entry.insert(0, account[3])  # account_type
        acc_type_entry.pack(pady=5)

        tk.Button(edit_account_window, text="Update Account", command=update_account).pack(pady=20)

    def delete_account(account_id):
        # Konfirmasi sebelum menghapus akun
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this account?")
        if confirm:
            # Menghapus akun yang dipilih
            conn = connect_db()
            c = conn.cursor()
            c.execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account successfully deleted.")
            display_accounts()

    # Popup utama untuk menampilkan daftar akun
    account_list_window = tk.Toplevel()
    account_list_window.title("Account List")

    # Treeview untuk menampilkan data akun
    columns = ("account_id", "account_number", "account_name", "account_type")
    tree = ttk.Treeview(account_list_window, columns=columns, show="headings")
    tree.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)

    # Tombol untuk menambah akun
    add_account_button = tk.Button(account_list_window, text="Add Account", command=add_account)
    add_account_button.pack(pady=10)

    # Fungsi untuk menangani klik baris dalam tabel
    def on_select(event):
        selected_item = tree.selection()[0]
        account_id = tree.item(selected_item)['values'][0]  # Ambil account_id
        action = messagebox.askquestion("Action", "Do you want to Edit or Delete this account?", icon='question')
        
        if action == 'yes':  # Edit
            edit_account(account_id)
        elif action == 'no':  # Delete
            delete_account(account_id)

    tree.bind("<Double-1>", on_select)  # Double-click untuk edit atau hapus

    # Memanggil dan menampilkan akun yang ada
    display_accounts()

# Fungsi untuk mencatat entri jurnal
def record_journal_entry():
    def save_journal():
        account_id = account_combobox.get()
        debit = debit_entry.get()
        credit = credit_entry.get()
        memo = memo_entry.get()

        if not debit and not credit:
            messagebox.showerror("Error", "Debit or Credit must be filled.")
            return

        conn = connect_db()
        c = conn.cursor()
        c.execute('''INSERT INTO journal_entries (account_id, debit, credit, memo) 
                     VALUES (?, ?, ?, ?)''', (account_id, debit, credit, memo))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Journal entry successfully recorded.")
        record_journal_window.destroy()

    record_journal_window = tk.Toplevel()
    record_journal_window.title("Record Journal Entry")

    # ComboBox untuk memilih akun
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT account_id, account_name FROM accounts")
    accounts = c.fetchall()
    conn.close()

    account_list = [account[1] for account in accounts]
    account_combobox = ttk.Combobox(record_journal_window, values=account_list, state="readonly")
    account_combobox.pack(pady=5)
    
    tk.Label(record_journal_window, text="Debit").pack(pady=5)
    debit_entry = tk.Entry(record_journal_window)
    debit_entry.pack(pady=5)

    tk.Label(record_journal_window, text="Credit").pack(pady=5)
    credit_entry = tk.Entry(record_journal_window)
    credit_entry.pack(pady=5)

    tk.Label(record_journal_window, text="Memo").pack(pady=5)
    memo_entry = tk.Entry(record_journal_window)
    memo_entry.pack(pady=5)

    tk.Button(record_journal_window, text="Save Journal Entry", command=save_journal).pack(pady=20)

# Fungsi untuk menampilkan jurnal transaksi
def transaction_journal():
    def filter_transactions():
        filter_date = date_filter_entry.get()
        conn = connect_db()
        c = conn.cursor()
        if filter_date:
            c.execute("SELECT * FROM transactions WHERE transaction_date LIKE ?", (filter_date+'%',))
        else:
            c.execute("SELECT * FROM transactions")
        rows = c.fetchall()
        conn.close()
        
        # Update Treeview
        for row in tree.get_children():
            tree.delete(row)
        
        for row in rows:
            tree.insert("", "end", values=row)

    transaction_journal_window = tk.Toplevel()
    transaction_journal_window.title("Transaction Journal")

    # Filter by Date
    tk.Label(transaction_journal_window, text="Filter by Date (YYYY-MM-DD):").pack(pady=5)
    date_filter_entry = tk.Entry(transaction_journal_window)
    date_filter_entry.pack(pady=5)
    
    tk.Button(transaction_journal_window, text="Filter", command=filter_transactions).pack(pady=10)

    # Treeview untuk menampilkan data transaksi
    columns = ("transaction_id", "transaction_date", "account_id", "amount", "description")
    tree = ttk.Treeview(transaction_journal_window, columns=columns, show="headings")
    tree.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)

    # Memanggil data awal
    filter_transactions()

# Fungsi untuk halaman General Ledger (kosongkan dulu)
def general_ledger():
    messagebox.showinfo("General Ledger", "Halaman General Ledger.")

# Halaman utama dengan tombol
def create_page(parent):
    create_table()  # Membuat tabel jika belum ada
    
    # Header dengan tema hijau
    header = tk.Label(parent, text="Halaman Akun", font=("Comic Sans MS", 18, "bold"), bg="#A8D5BA", fg="white", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Frame untuk tombol-tombol utama
    frame_buttons = tk.Frame(parent)
    frame_buttons.pack(pady=20, fill="x")

    # Tombol Account List
    account_list_button = tk.Button(frame_buttons, text="Account List", font=("Comic Sans MS", 12), command=account_list)
    account_list_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol Record Journal Entry
    record_journal_button = tk.Button(frame_buttons, text="Record Journal Entry", font=("Comic Sans MS", 12), command=record_journal_entry)
    record_journal_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol Transaction Journal
    transaction_journal_button = tk.Button(frame_buttons, text="Transaction Journal", font=("Comic Sans MS", 12), command=transaction_journal)
    transaction_journal_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol General Ledger
    general_ledger_button = tk.Button(frame_buttons, text="General Ledger", font=("Comic Sans MS", 12), command=general_ledger)
    general_ledger_button.pack(side="left", padx=10, fill="x", expand=True)
