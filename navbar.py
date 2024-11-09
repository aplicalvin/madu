import tkinter as tk
from tkinter import ttk
import importlib

# Fungsi untuk membuat sidebar/navbar
def create_sidebar(window, frame_content, current_page):
    # Frame Sidebar
    frame_sidebar = tk.Frame(window, width=300, bg="sky blue", height=window.winfo_height())
    frame_sidebar.grid(row=0, column=0, sticky="ns")  # Use grid instead of pack

    # Tombol Navigasi - Tombol main di atas
    button_main = ttk.Button(frame_sidebar, text="Main", command=lambda: update_page(window, frame_content, "main", current_page))
    button_main.grid(row=0, column=0, pady=10, sticky="ew")

    # Tombol Navigasi lainnya
    button_buku_besar = ttk.Button(frame_sidebar, text="Buku Besar", command=lambda: update_page(window, frame_content, "buku_besar", current_page))
    button_buku_besar.grid(row=1, column=0, pady=10, sticky="ew")

    button_neraca_saldo = ttk.Button(frame_sidebar, text="Neraca Saldo", command=lambda: update_page(window, frame_content, "neraca_saldo", current_page))
    button_neraca_saldo.grid(row=2, column=0, pady=10, sticky="ew")

    button_laba_rugi = ttk.Button(frame_sidebar, text="Laporan Laba Rugi", command=lambda: update_page(window, frame_content, "laba_rugi", current_page))
    button_laba_rugi.grid(row=3, column=0, pady=10, sticky="ew")

    button_ekuitas = ttk.Button(frame_sidebar, text="Laporan Ekuitas", command=lambda: update_page(window, frame_content, "ekuitas", current_page))
    button_ekuitas.grid(row=4, column=0, pady=10, sticky="ew")

    return frame_sidebar

# Fungsi untuk memperbarui halaman sesuai dengan pilihan di sidebar
def update_page(window, frame_content, page_name, current_page):
    # Hanya lakukan perubahan halaman jika halaman yang dipilih berbeda
    if page_name != current_page:
        # Hapus konten lama
        for widget in frame_content.winfo_children():
            widget.destroy()

        # Memuat halaman baru berdasarkan nama halaman
        load_page(window, frame_content, page_name)

    return page_name

# Fungsi untuk memuat halaman berdasarkan nama
def load_page(window, frame_content, page_name):
    # Coba import file halaman dengan menggunakan importlib
    try:
        # Import halaman sesuai dengan nama file (misalnya buku_besar.py menjadi buku_besar)
        page_module = importlib.import_module(f"pages.{page_name}")
        page_module.create_page(frame_content)  # Setiap halaman harus punya fungsi create_page
    except ModuleNotFoundError:
        print(f"Halaman {page_name} tidak ditemukan.")
