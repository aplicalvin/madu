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
    return pendapatan, total_pendapatan, beban_usaha, total_beban, laba

# Fungsi untuk membuat tampilan halaman laporan laba/rugi
def create_page(parent):
    # Ambil data laporan laba/rugi
    pendapatan, total_pendapatan, beban_usaha, total_beban, laba = get_laporan_laba_rugi()

    # Frame untuk judul
    header = tk.Label(parent, text="Laporan Keuangan Laba Rugi", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Membuat tabel untuk pendapatan usaha
    frame_pendapatan = tk.Frame(parent)
    frame_pendapatan.pack(fill="x", pady=5)

    pendapatan_label = tk.Label(frame_pendapatan, text="Pendapatan Usaha", font=("Arial", 14), anchor="w")
    pendapatan_label.pack(fill="x", pady=5)

    for akun in pendapatan:
        akun_label = tk.Label(frame_pendapatan, text=f"{akun[1]} ({akun[0]})", font=("Arial", 12), anchor="w")
        akun_label.pack(fill="x", padx=10)

        # Query untuk mendapatkan total saldo (kredit/debit) akun ini
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT SUM(kredit) - SUM(debet) FROM data_akuntansi WHERE no_akun = ?", (akun[0],))
        saldo = c.fetchone()[0]
        saldo_label = tk.Label(frame_pendapatan, text=f"{saldo if saldo else 0}", font=("Arial", 12), anchor="w")
        saldo_label.pack(fill="x", padx=20)
        conn.close()

    # Tabel untuk beban usaha
    frame_beban = tk.Frame(parent)
    frame_beban.pack(fill="x", pady=5)

    beban_label = tk.Label(frame_beban, text="Beban Usaha", font=("Arial", 14), anchor="w")
    beban_label.pack(fill="x", pady=5)

    for akun in beban_usaha:
        akun_label = tk.Label(frame_beban, text=f"{akun[1]} ({akun[0]})", font=("Arial", 12), anchor="w")
        akun_label.pack(fill="x", padx=10)

        # Query untuk mendapatkan total saldo (debet/kredit) akun ini
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT SUM(debet) - SUM(kredit) FROM data_akuntansi WHERE no_akun = ?", (akun[0],))
        saldo = c.fetchone()[0]
        saldo_label = tk.Label(frame_beban, text=f"{saldo if saldo else 0}", font=("Arial", 12), anchor="w")
        saldo_label.pack(fill="x", padx=20)
        conn.close()

    # Menampilkan jumlah beban usaha
    jumlah_beban_label = tk.Label(parent, text=f"Jumlah Beban Usaha: {total_beban}", font=("Arial", 14), anchor="w")
    jumlah_beban_label.pack(fill="x", pady=5)

    # Menampilkan laba/rugi
    laba_label = tk.Label(parent, text=f"Laba: {laba}", font=("Arial", 14), anchor="w", fg="green" if laba > 0 else "red")
    laba_label.pack(fill="x", pady=5)


