import tkinter as tk
from tkinter import ttk
import sqlite3

# Fungsi untuk mengambil data berdasarkan No. Akun
def get_data_by_account(account_number):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data_akuntansi WHERE no_akun = ?", (account_number,))
    data = c.fetchall()
    conn.close()
    return data

# Fungsi untuk menghitung total debit dan kredit per No. Akun
def hitung_total(data):
    total_debit = sum(row[5] for row in data)  # Kolom debet
    total_kredit = sum(row[6] for row in data)  # Kolom kredit
    return total_debit, total_kredit

# Fungsi untuk mengambil Nama Rekening berdasarkan No. Akun dari data manual
def get_account_name(account_number):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Query untuk mengambil nama rekening berdasarkan no_akun
    c.execute("SELECT nama_rekening FROM akun WHERE no_akun = ?", (account_number,))
    result = c.fetchone()  # Ambil hasil pertama (harusnya hanya ada satu)

    conn.close()

    # Jika ditemukan, kembalikan nama rekening, jika tidak ada, kembalikan "Tidak Ditemukan"
    return result[0] if result else "Tidak Ditemukan"


# Fungsi untuk menampilkan data dalam satu tabel yang meringkas semua akun
def tampilkan_data(tree_frame):
    # Hapus semua widget sebelumnya
    for widget in tree_frame.winfo_children():
        widget.destroy()

    # Ambil data untuk semua No. Akun
    accounts = get_unique_accounts()

    # Judul untuk tabel ringkasan
    label_account = tk.Label(tree_frame, text="Ringkasan Neraca Saldo", font=("Arial", 14, "bold"))
    label_account.pack(pady=5)

    # Tabel untuk menampilkan data
    columns = ("No. Rek", "Nama Rekening", "Debit", "Kredit")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(pady=10)

    total_debit_all = 0
    total_kredit_all = 0

    # Menampilkan data untuk setiap No. Akun
    for account in accounts:
        # Ambil data transaksi untuk No. Akun ini
        data = get_data_by_account(account)

        # Hitung total debit dan kredit untuk akun ini
        total_debit, total_kredit = hitung_total(data)

        # Hitung selisih antara total kredit dan total debit
        selisih = total_kredit - total_debit

        # Tentukan nilai yang akan dimasukkan ke kolom Debit dan Kredit berdasarkan selisih
        if selisih > 0:
            debit = 0
            kredit = selisih
        elif selisih < 0:
            debit = abs(selisih)  # Negatif, jadi kita ambil nilai positifnya
            kredit = 0
        else:
            debit = 0
            kredit = 0

        # Ambil Nama Rekening berdasarkan No. Akun dari data manual
        account_name = get_account_name(account)

        # Masukkan data ke dalam tabel
        tree.insert('', 'end', values=(account, account_name, debit, kredit))

        # Tambahkan total untuk semuanya
        total_debit_all += debit
        total_kredit_all += kredit

    # Menampilkan total keseluruhan di bawah tabel
    total_frame = tk.Frame(tree_frame)
    total_frame.pack(pady=5)

    label_total_debit = tk.Label(total_frame, text=f"Total Debit: {total_debit_all}")
    label_total_debit.grid(row=0, column=0, padx=10)

    label_total_kredit = tk.Label(total_frame, text=f"Total Kredit: {total_kredit_all}")
    label_total_kredit.grid(row=0, column=1, padx=10)

    # Menambahkan baris untuk JUMLAH
    tree.insert('', 'end', values=('JUMLAH', '', total_debit_all, total_kredit_all))


# Fungsi untuk mengambil semua No. Akun unik dari database
def get_unique_accounts():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT no_akun FROM data_akuntansi")
    accounts = c.fetchall()
    conn.close()
    return [account[0] for account in accounts]

# Fungsi untuk membuat halaman utama
def create_page(parent):
    # Frame untuk judul
    header = tk.Label(parent, text="Ringkasan Neraca Saldo", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Buat canvas dan scrollbar untuk menggulir seluruh halaman
    canvas = tk.Canvas(parent)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Letakkan canvas dan scrollbar di frame
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Buat frame untuk menampung semua tabel dalam canvas
    page_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=page_frame, anchor="nw")

    # Tampilkan ringkasan data
    tampilkan_data(page_frame)

    # Update scrollregion untuk canvas setelah semua data dimasukkan
    page_frame.update_idletasks()  # Update layout
    canvas.config(scrollregion=canvas.bbox("all"))  # Tentukan area yang dapat discroll

# Membuat window utama untuk menjalankan aplikasi
def main():
    root = tk.Tk()
    root.title("Aplikasi Neraca Saldo")
    root.geometry("800x600")
    
    # Buat halaman utama
    create_page(root)

    # Jalankan aplikasi
    root.mainloop()

# Menjalankan aplikasi
if __name__ == "__main__":
    main()
