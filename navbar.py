import tkinter as tk
from tkinter import ttk
import importlib
import sys
from tkinter import font

# Menambahkan folder pages ke sys.path agar bisa ditemukan oleh importlib
sys.path.append('./pages')  # Pastikan folder 'pages' ada di jalur yang benar

# Fungsi untuk membuat sidebar/navbar
def create_sidebar(window, frame_content, current_page):
    # Frame Sidebar dengan warna hijau muda
    frame_sidebar = tk.Frame(window, width=300, bg="#A8D5BA", height=window.winfo_height())
    frame_sidebar.grid(row=0, column=0, sticky="ns")  # Gunakan grid alih-alih pack

    # Menentukan style untuk tombol dengan font Comic Sans MS
    button_style = ttk.Style()
    button_style.configure("TButton",
                           font=("Comic Sans MS", 12, "bold"),  # Menggunakan Comic Sans MS dengan bold
                           padding=10,
                           relief="flat",  # Menghilangkan border pada tombol
                           background="#A8D5BA",  # Warna hijau muda untuk tombol
                           foreground="black")

    # Menambahkan efek hover untuk tombol
    button_style.map("TButton", 
                     background=[('active', '#7FB5B5')])  # Warna lebih gelap saat hover

    # Fungsi untuk membuat tombol dengan sudut rounded
    def create_rounded_button(parent, text, row, col, command):
        button = ttk.Button(parent, text=text, style="TButton", command=command)
        button.grid(row=row, column=col, pady=10, sticky="ew")
        
        # Styling tombol untuk rounded corners
        button.configure(width=15)  # Menentukan lebar tombol agar sudut lebih jelas
        button.grid_configure(padx=10, pady=5)
        return button

    # Tombol Navigasi - Setiap tombol memiliki baris yang unik pada grid
    button_buku_besar = create_rounded_button(frame_sidebar, "Inventory", 1, 0, 
                                              lambda: update_page(window, frame_content, "inventory", current_page))
    button_jurnal = create_rounded_button(frame_sidebar, "Accounts", 2, 0, 
                                          lambda: update_page(window, frame_content, "accounts", current_page))
    button_neraca_saldo = create_rounded_button(frame_sidebar, "banking", 3, 0, 
                                                lambda: update_page(window, frame_content, "banking", current_page))
    button_laba_rugi = create_rounded_button(frame_sidebar, "Sales", 4, 0, 
                                             lambda: update_page(window, frame_content, "sales", current_page))
    button_ekuitas = create_rounded_button(frame_sidebar, "Purchase", 5, 0, 
                                           lambda: update_page(window, frame_content, "purchase", current_page))

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

        # Update current_page setelah memuat halaman baru
        current_page = page_name

    return current_page  # Pastikan current_page ter-update dengan benar

# Fungsi untuk memuat halaman berdasarkan nama
def load_page(window, frame_content, page_name):
    # Coba import file halaman dengan menggunakan importlib
    try:
        # Import halaman sesuai dengan nama file (misalnya buku_besar.py menjadi buku_besar)
        page_module = importlib.import_module(f"pages.{page_name}")
        page_module.create_page(frame_content)  # Setiap halaman harus punya fungsi create_page
    except ModuleNotFoundError:
        print(f"Halaman {page_name} tidak ditemukan.")
