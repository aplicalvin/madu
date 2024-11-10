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

    # Tabel untuk Sales
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sales_type TEXT,
                    journal_memo TEXT,
                    referral_source TEXT,
                    invoice_delivery_status TEXT,
                    paid_today REAL,
                    payment_method TEXT,
                    balance_due REAL,
                    date DATE DEFAULT CURRENT_DATE)''')

    # Tabel untuk Purchases
    c.execute('''CREATE TABLE IF NOT EXISTS purchases (
                    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    purchase_type TEXT,
                    purchase_no TEXT,
                    date DATE DEFAULT CURRENT_DATE,
                    supplier_invoice_no TEXT,
                    subtotal REAL,
                    paid_today REAL,
                    balance_due REAL)''')

    # Tabel untuk Transaction Journal
    c.execute('''CREATE TABLE IF NOT EXISTS transaction_journal (
                    journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_type TEXT,
                    amount REAL NOT NULL,
                    memo TEXT,
                    date DATE DEFAULT CURRENT_DATE)''')

    conn.commit()
    conn.close()

# Fungsi untuk Enter Sales
def enter_sales():
    def save_sales():
        sales_type = sales_type_var.get()
        journal_memo = journal_memo_entry.get()
        referral_source = referral_source_entry.get()
        invoice_delivery_status = invoice_status_entry.get()
        paid_today = float(paid_today_entry.get()) if paid_today_entry.get() else 0
        payment_method = payment_method_entry.get()
        balance_due = float(balance_due_entry.get()) if balance_due_entry.get() else 0
        date = date_entry.get()

        # Simpan data sales ke database
        conn = connect_db()
        c = conn.cursor()
        c.execute('''INSERT INTO sales (sales_type, journal_memo, referral_source, invoice_delivery_status, paid_today, payment_method, balance_due, date)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (sales_type, journal_memo, referral_source, invoice_delivery_status, paid_today, payment_method, balance_due, date))
        conn.commit()

        # Tambahkan ke transaction journal
        c.execute('''INSERT INTO transaction_journal (transaction_type, amount, memo, date)
                     VALUES (?, ?, ?, ?)''', ('Sale', balance_due, journal_memo, date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Sales Data Saved Successfully")
        display_sales_data()

    def display_sales_data():
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM sales")
        rows = c.fetchall()
        conn.close()

        # Menghapus data lama di Treeview
        for row in tree_sales.get_children():
            tree_sales.delete(row)

        # Menambahkan data sales ke Treeview
        for row in rows:
            tree_sales.insert("", "end", values=row)

    # Form untuk Enter Sales
    sales_window = tk.Toplevel()
    sales_window.title("Enter Sales")

    # Checkbox Sales Type
    sales_type_var = tk.StringVar()
    tk.Label(sales_window, text="Sales Type").pack(pady=5)
    retail_rb = tk.Radiobutton(sales_window, text="Retail", variable=sales_type_var, value="Retail")
    wholesale_rb = tk.Radiobutton(sales_window, text="Wholesale", variable=sales_type_var, value="Wholesale")
    retail_rb.pack(pady=5)
    wholesale_rb.pack(pady=5)

    tk.Label(sales_window, text="Journal Memo").pack(pady=5)
    journal_memo_entry = tk.Entry(sales_window)
    journal_memo_entry.pack(pady=5)

    tk.Label(sales_window, text="Referral Source").pack(pady=5)
    referral_source_entry = tk.Entry(sales_window)
    referral_source_entry.pack(pady=5)

    tk.Label(sales_window, text="Invoice Delivery Status").pack(pady=5)
    invoice_status_entry = tk.Entry(sales_window)
    invoice_status_entry.pack(pady=5)

    tk.Label(sales_window, text="Paid Today").pack(pady=5)
    paid_today_entry = tk.Entry(sales_window)
    paid_today_entry.pack(pady=5)

    tk.Label(sales_window, text="Payment Method").pack(pady=5)
    payment_method_entry = tk.Entry(sales_window)
    payment_method_entry.pack(pady=5)

    tk.Label(sales_window, text="Balance Due").pack(pady=5)
    balance_due_entry = tk.Entry(sales_window)
    balance_due_entry.pack(pady=5)

    tk.Label(sales_window, text="Date (YYYY-MM-DD)").pack(pady=5)
    date_entry = tk.Entry(sales_window)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default date is today
    date_entry.pack(pady=5)

    tk.Button(sales_window, text="Save Sales", command=save_sales).pack(pady=20)

    # Tabel untuk menampilkan data sales
    columns = ("sale_id", "sales_type", "journal_memo", "referral_source", "invoice_delivery_status", "paid_today", "payment_method", "balance_due", "date")
    tree_sales = ttk.Treeview(sales_window, columns=columns, show="headings")
    tree_sales.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree_sales.heading(col, text=col)

    display_sales_data()

# Fungsi untuk Enter Purchases
def enter_purchases():
    def save_purchases():
        purchase_type = purchase_type_entry.get()
        purchase_no = purchase_no_entry.get()
        date = date_entry.get()
        supplier_invoice_no = supplier_invoice_no_entry.get()
        subtotal = float(subtotal_entry.get()) if subtotal_entry.get() else 0
        paid_today = float(paid_today_entry.get()) if paid_today_entry.get() else 0
        balance_due = float(balance_due_entry.get()) if balance_due_entry.get() else 0

        # Simpan data purchases ke database
        conn = connect_db()
        c = conn.cursor()
        c.execute('''INSERT INTO purchases (purchase_type, purchase_no, date, supplier_invoice_no, subtotal, paid_today, balance_due)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (purchase_type, purchase_no, date, supplier_invoice_no, subtotal, paid_today, balance_due))
        conn.commit()

        # Tambahkan ke transaction journal
        c.execute('''INSERT INTO transaction_journal (transaction_type, amount, memo, date)
                     VALUES (?, ?, ?, ?)''', ('Purchase', balance_due, purchase_no, date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Purchase Data Saved Successfully")
        display_purchases_data()

    def display_purchases_data():
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM purchases")
        rows = c.fetchall()
        conn.close()

        # Menghapus data lama di Treeview
        for row in tree_purchases.get_children():
            tree_purchases.delete(row)

        # Menambahkan data purchases ke Treeview
        for row in rows:
            tree_purchases.insert("", "end", values=row)

    # Form untuk Enter Purchases
    purchases_window = tk.Toplevel()
    purchases_window.title("Enter Purchases")

    tk.Label(purchases_window, text="Purchase Type").pack(pady=5)
    purchase_type_entry = tk.Entry(purchases_window)
    purchase_type_entry.pack(pady=5)

    tk.Label(purchases_window, text="Purchase No").pack(pady=5)
    purchase_no_entry = tk.Entry(purchases_window)
    purchase_no_entry.pack(pady=5)

    tk.Label(purchases_window, text="Supplier Invoice No").pack(pady=5)
    supplier_invoice_no_entry = tk.Entry(purchases_window)
    supplier_invoice_no_entry.pack(pady=5)

    tk.Label(purchases_window, text="Subtotal").pack(pady=5)
    subtotal_entry = tk.Entry(purchases_window)
    subtotal_entry.pack(pady=5)

    tk.Label(purchases_window, text="Paid Today").pack(pady=5)
    paid_today_entry = tk.Entry(purchases_window)
    paid_today_entry.pack(pady=5)

    tk.Label(purchases_window, text="Balance Due").pack(pady=5)
    balance_due_entry = tk.Entry(purchases_window)
    balance_due_entry.pack(pady=5)

    tk.Label(purchases_window, text="Date (YYYY-MM-DD)").pack(pady=5)
    date_entry = tk.Entry(purchases_window)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default date is today
    date_entry.pack(pady=5)

    tk.Button(purchases_window, text="Save Purchase", command=save_purchases).pack(pady=20)

    # Tabel untuk menampilkan data purchases
    columns = ("purchase_id", "purchase_type", "purchase_no", "date", "supplier_invoice_no", "subtotal", "paid_today", "balance_due")
    tree_purchases = ttk.Treeview(purchases_window, columns=columns, show="headings")
    tree_purchases.pack(pady=20, fill="both", expand=True)

    for col in columns:
        tree_purchases.heading(col, text=col)

    display_purchases_data()

# Fungsi untuk Transaction Journal
def transaction_journal():
    def display_transactions():
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

# Fungsi untuk halaman Sales & Purchases
def create_page(parent):
    create_table()  # Membuat tabel jika belum ada

    # Header dengan tema hijau
    header = tk.Label(parent, text="Halaman Sales & Purchases", font=("Comic Sans MS", 18, "bold"), bg="#A8D5BA", fg="white", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Frame untuk tombol-tombol utama
    frame_buttons = tk.Frame(parent)
    frame_buttons.pack(pady=20, fill="x")

    # Tombol Enter Sales
    enter_sales_button = tk.Button(frame_buttons, text="Enter Sales", font=("Comic Sans MS", 12), command=enter_sales)
    enter_sales_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol Enter Purchases
    enter_purchases_button = tk.Button(frame_buttons, text="Enter Purchases", font=("Comic Sans MS", 12), command=enter_purchases)
    enter_purchases_button.pack(side="left", padx=10, fill="x", expand=True)

    # Tombol Transaction Journal
    transaction_journal_button = tk.Button(frame_buttons, text="Transaction Journal", font=("Comic Sans MS", 12), command=transaction_journal)
    transaction_journal_button.pack(side="left", padx=10, fill="x", expand=True)
