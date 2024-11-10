import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Membuka koneksi ke database
def connect_db():
    return sqlite3.connect('banking.db')

# Membuat tabel jika belum ada
def create_table():
    conn = connect_db()
    c = conn.cursor()

    # Tabel untuk Cash Payments
    c.execute('''CREATE TABLE IF NOT EXISTS cash_payments (
                    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card TEXT,
                    pay REAL NOT NULL,
                    memo TEXT,
                    cheque_no TEXT,
                    date DATE DEFAULT CURRENT_DATE,
                    amount REAL NOT NULL)''')

    # Tabel untuk Cash Receipts
    c.execute('''CREATE TABLE IF NOT EXISTS cash_receipts (
                    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    memo TEXT,
                    id_no TEXT NOT NULL,
                    date DATE DEFAULT CURRENT_DATE)''')

    # Tabel untuk Transaction Journal
    c.execute('''CREATE TABLE IF NOT EXISTS transaction_journal (
                    journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_type TEXT NOT NULL,  -- 'Payment' or 'Receipt'
                    amount REAL NOT NULL,
                    memo TEXT,
                    date DATE DEFAULT CURRENT_DATE)''')

    conn.commit()
    conn.close()

# Fungsi untuk Cash Payment
def cash_payment():
    def save_cash_payment():
        card = card_entry.get()
        pay = pay_entry.get()
        memo = memo_entry.get()
        cheque_no = cheque_no_entry.get()
        amount = amount_entry.get()
        date = date_entry.get()

        if not pay or not amount:
            messagebox.showerror("Error", "Payment and Amount are required.")
            return

        # Simpan data cash payment ke database
        conn = connect_db()
        c = conn.cursor()
        c.execute('''INSERT INTO cash_payments (card, pay, memo, cheque_no, date, amount)
                     VALUES (?, ?, ?, ?, ?, ?)''', (card, pay, memo, cheque_no, date, amount))
        conn.commit()
        conn.close()

        # Jurnal transaksi untuk cash payment
        c.execute('''INSERT INTO transaction_journal (transaction_type, amount, memo, date)
                     VALUES (?, ?, ?, ?)''', ('Payment', amount, memo, date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Cash Payment Recorded")
        display_cash_payments()

    def display_cash_payments():
        # Menampilkan data cash payments di tabel
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM cash_payments")
        rows = c.fetchall()
        conn.close()

        # Menghapus data lama di Treeview
        for row in tree_cash_payments.get_children():
            tree_cash_payments.delete(row)

        # Menambahkan data cash payments ke Treeview
        for row in rows:
            tree_cash_payments.insert("", "end", values=row)

    # Form untuk Cash Payment
    payment_window = tk.Toplevel()
    payment_window.title("Cash Payment")

    tk.Label(payment_window, text="Card").pack(pady=5)
    card_entry = tk.Entry(payment_window)
    card_entry.pack(pady=5)

    tk.Label(payment_window, text="Pay").pack(pady=5)
    pay_entry = tk.Entry(payment_window)
    pay_entry.pack(pady=5)

    tk.Label(payment_window, text="Memo").pack(pady=5)
    memo_entry = tk.Entry(payment_window)
    memo_entry.pack(pady=5)

    tk.Label(payment_window, text="Cheque No").pack(pady=5)
    cheque_no_entry = tk.Entry(payment_window)
    cheque_no_entry.pack(pady=5)

    tk.Label(payment_window, text="Amount").pack(pady=5)
    amount_entry = tk.Entry(payment_window)
    amount_entry.pack(pady=5)

    tk.Label(payment_window, text="Date (YYYY-MM-DD)").pack(pady=5)
    date_entry = tk.Entry(payment_window)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default date is today
    date_entry.pack(pady=5)

    tk.Button(payment_window, text="Save Cash Payment", command=save_cash_payment).pack(pady=20)

    # Tabel untuk menampilkan data cash payments
    columns = ("payment_id", "card", "pay", "memo", "cheque_no", "date", "amount")
    tree_cash_payments = ttk.Treeview(payment_window, columns=columns, show="headings")
    tree_cash_payments.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree_cash_payments.heading(col, text=col)

    display_cash_payments()

# Fungsi untuk Cash Receipt
def cash_receipt():
    def save_cash_receipt():
        amount = amount_entry.get()
        payment_method = payment_method_entry.get()
        memo = memo_entry.get()
        id_no = id_no_entry.get()
        date = date_entry.get()

        if not amount:
            messagebox.showerror("Error", "Amount is required.")
            return

        # Simpan data cash receipt ke database
        conn = connect_db()
        c = conn.cursor()
        c.execute('''INSERT INTO cash_receipts (amount, payment_method, memo, id_no, date)
                     VALUES (?, ?, ?, ?, ?)''', (amount, payment_method, memo, id_no, date))
        conn.commit()
        conn.close()

        # Jurnal transaksi untuk cash receipt
        c.execute('''INSERT INTO transaction_journal (transaction_type, amount, memo, date)
                     VALUES (?, ?, ?, ?)''', ('Receipt', amount, memo, date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Cash Receipt Recorded")
        display_cash_receipts()

    def display_cash_receipts():
        # Menampilkan data cash receipts di tabel
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM cash_receipts")
        rows = c.fetchall()
        conn.close()

        # Menghapus data lama di Treeview
        for row in tree_cash_receipts.get_children():
            tree_cash_receipts.delete(row)

        # Menambahkan data cash receipts ke Treeview
        for row in rows:
            tree_cash_receipts.insert("", "end", values=row)

    # Form untuk Cash Receipt
    receipt_window = tk.Toplevel()
    receipt_window.title("Cash Receipt")

    tk.Label(receipt_window, text="Amount").pack(pady=5)
    amount_entry = tk.Entry(receipt_window)
    amount_entry.pack(pady=5)

    tk.Label(receipt_window, text="Payment Method").pack(pady=5)
    payment_method_entry = tk.Entry(receipt_window)
    payment_method_entry.pack(pady=5)

    tk.Label(receipt_window, text="Memo").pack(pady=5)
    memo_entry = tk.Entry(receipt_window)
    memo_entry.pack(pady=5)

    tk.Label(receipt_window, text="ID No").pack(pady=5)
    id_no_entry = tk.Entry(receipt_window)
    id_no_entry.pack(pady=5)

    tk.Label(receipt_window, text="Date (YYYY-MM-DD)").pack(pady=5)
    date_entry = tk.Entry(receipt_window)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default date is today
    date_entry.pack(pady=5)

    tk.Button(receipt_window, text="Save Cash Receipt", command=save_cash_receipt).pack(pady=20)

    # Tabel untuk menampilkan data cash receipts
    columns = ("receipt_id", "amount", "payment_method", "memo", "id_no", "date")
    tree_cash_receipts = ttk.Treeview(receipt_window, columns=columns, show="headings")
    tree_cash_receipts.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree_cash_receipts.heading(col, text=col)

    display_cash_receipts()

# Fungsi untuk Transaction Journal
def transaction_journal():
    def display_transactions():
        # Menampilkan semua transaksi di transaction journal
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM transaction_journal")
        rows = c.fetchall()
        conn.close()

        # Menghapus data lama di Treeview
        for row in tree_transactions.get_children():
            tree_transactions.delete(row)

        # Menambahkan transaksi ke Treeview
        for row in rows:
            tree_transactions.insert("", "end", values=row)

    journal_window = tk.Toplevel()
    journal_window.title("Transaction Journal")

    # Tabel untuk menampilkan transaction journal
    columns = ("journal_id", "transaction_type", "amount", "memo", "date")
    tree_transactions = ttk.Treeview(journal_window, columns=columns, show="headings")
    tree_transactions.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree_transactions.heading(col, text=col)

    display_transactions()

# Fungsi untuk halaman Banking
def create_page(parent):
    create_table()  # Membuat tabel jika belum ada
    
    # Header dengan tema hijau
    header = tk.Label(parent, text="Halaman Banking", font=("Comic Sans MS", 18, "bold"), bg="#A8D5BA", fg="white", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Frame untuk tombol-tombol utama
    frame_buttons = tk.Frame(parent)
    frame_buttons.pack(pady=20, fill="x")

    # Tombol Cash Payment
    cash_payment_button = tk.Button(frame_buttons, text="Cash Payment", font=("Comic Sans MS", 12), command=cash_payment)
    cash_payment_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol Cash Receipt
    cash_receipt_button = tk.Button(frame_buttons, text="Cash Receipt", font=("Comic Sans MS", 12), command=cash_receipt)
    cash_receipt_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol Transaction Journal
    transaction_journal_button = tk.Button(frame_buttons, text="Transaction Journal", font=("Comic Sans MS", 12), command=transaction_journal)
    transaction_journal_button.pack(side="left", padx=10, fill="x", expand=True)
