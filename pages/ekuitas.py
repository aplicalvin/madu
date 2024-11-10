import sqlite3
import tkinter as tk
from tkinter import ttk

# Fungsi untuk mendapatkan laporan laba/rugi
def get_laporan_laba_rugi():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Mengambil data akun pendapatan (nomor akun 401)
    c.execute("SELECT no_akun, nama_rekening FROM akun WHERE no_akun = '401'")
    pendapatan = c.fetchall()

    # Mengambil data akun beban usaha (beban = 1)
    c.execute("SELECT no_akun, nama_rekening FROM akun WHERE beban = 1")
    beban_usaha = c.fetchall()

    # Menghitung total pendapatan
    total_pendapatan = 0
    for akun in pendapatan:
        no_akun = akun[0]
        c.execute("SELECT SUM(kredit) - SUM(debet) FROM data_akuntansi WHERE no_akun = ?", (no_akun,))
        saldo = c.fetchone()[0]
        total_pendapatan += saldo if saldo else 0

    # Menghitung total beban
    total_beban = 0
    for akun in beban_usaha:
        no_akun = akun[0]
        c.execute("SELECT SUM(debet) - SUM(kredit) FROM data_akuntansi WHERE no_akun = ?", (no_akun,))
        saldo = c.fetchone()[0]
        total_beban += saldo if saldo else 0

    # Menghitung laba
    laba = total_pendapatan - total_beban

    conn.close()

    # Mengembalikan hasil perhitungan
    return laba

# Fungsi untuk membuat tampilan halaman laporan laba/rugi
def create_page(parent):
    # Ambil data laporan laba/rugi
    laba = get_laporan_laba_rugi()

    # Frame untuk judul
    header = tk.Label(parent, text="Laporan Keuangan Ekuitas", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Menampilkan laba bersih
    laba_label = tk.Label(parent, text=f"Laba Bersih: {laba}", font=("Arial", 14), anchor="w", fg="green" if laba > 0 else "red")
    laba_label.pack(fill="x", pady=5)

    # Frame untuk input Modal
    frame_modal = tk.Frame(parent)
    frame_modal.pack(fill="x", pady=10)

    modal_label = tk.Label(frame_modal, text="Modal Awal: ", font=("Arial", 14), anchor="w")
    modal_label.pack(fill="x", padx=10)

    # Input untuk modal
    modal_entry = tk.Entry(frame_modal, font=("Arial", 12))
    modal_entry.pack(fill="x", padx=10)
    modal_entry.insert(0, "0")  # default value, bisa disesuaikan

    # Fungsi untuk menghitung Modal Sekarang
    def calculate_modal_sekarang():
        try:
            modal_awal = float(modal_entry.get())
            modal_sekarang = modal_awal + laba
            modal_sekarang_label.config(text=f"Modal Sekarang: {modal_sekarang}")
        except ValueError:
            modal_sekarang_label.config(text="Input Modal tidak valid!")

    # Tombol untuk menghitung modal sekarang
    hitung_button = tk.Button(frame_modal, text="Hitung Modal Sekarang", font=("Arial", 12), command=calculate_modal_sekarang)
    hitung_button.pack(fill="x", pady=10)

    # Label untuk menampilkan Modal Sekarang
    modal_sekarang_label = tk.Label(parent, text="Modal Sekarang: 0", font=("Arial", 14), anchor="w")
    modal_sekarang_label.pack(fill="x", pady=5)
