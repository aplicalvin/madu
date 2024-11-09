import tkinter as tk
from tkinter import ttk

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
    if page_name != current_page:
        current_page = load_page(window, frame_content, page_name, current_page)
    return current_page

# Fungsi untuk memuat halaman sesuai dengan pilihan di sidebar
def load_page(window, frame_content, page_name, current_page):
    # Bersihkan frame konten lama hanya jika halaman berbeda
    if page_name != current_page:
        for widget in frame_content.winfo_children():
            widget.destroy()

    # Panggil halaman yang sesuai
    if page_name == "main":
        from main import load_page 
        # aku ingin ketika main dijalankan, dia akan nge load function pertama di halaman main 
        load_page(window, frame_content)
    elif page_name == "buku_besar":
        from pages.buku_besar import load_page
        load_page(window, frame_content)
    elif page_name == "neraca_saldo":
        from pages.neraca_saldo import load_page
        load_page(window, frame_content)
    elif page_name == "laba_rugi":
        from pages.laba_rugi import load_page
        load_page(window, frame_content)
    elif page_name == "ekuitas":
        from pages.ekuitas import load_page
        load_page(window, frame_content)

    # Update current page untuk memastikan navigasi berfungsi
    current_page = page_name
    return current_page
