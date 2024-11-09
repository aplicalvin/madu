# main.py
import tkinter as tk
from navbar import create_sidebar  # Mengimpor sidebar/navbar dari navbar.py
from style import apply_styles

# GUI utama
window = tk.Tk()
window.title("Program Aplikasi Akuntansi")
window.geometry("1200x600")

# Terapkan styling dari file style.py
apply_styles(window)

# Frame utama untuk layout (menggunakan grid untuk lebih fleksibel)
window.grid_rowconfigure(0, weight=1)  # Agar konten mengisi seluruh tinggi
window.grid_columnconfigure(1, weight=1)  # Kolom konten utama memiliki bobot lebih besar

# Frame konten utama (di kanan)
frame_content = tk.Frame(window, bg="white")
frame_content.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# Membuat sidebar di kiri
current_page = "dashboard"  # Set halaman default
create_sidebar(window, frame_content, current_page)

# Menjalankan aplikasi
window.mainloop()
